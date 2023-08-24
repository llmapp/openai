import { useEffect, useRef, useState } from "react";
import type { Options, RecordRTCPromisesHandler } from "recordrtc";
import { Harker } from "hark";

const defaultConfig = { streaming: true, samplingRate: 16000, timeSlice: 5_000 };

export const useRTC: UseRTCHook = (config?: UseRTCConfig) => {
  const { samplingRate, streaming, timeSlice, onDataAvailable: onDataAvailableCallback } = { ...defaultConfig, ...config };
  const chunks = useRef<Blob[]>([]);
  const listener = useRef<Harker>();
  const recorder = useRef<RecordRTCPromisesHandler>();
  const stream = useRef<MediaStream>();

  const [recording, setRecording] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [blob, setBlob] = useState<Blob>();

  useEffect(() => {
    return () => {
      if (chunks.current) {
        chunks.current = [];
      }
      if (recorder.current) {
        recorder.current.destroy();
        recorder.current = undefined;
      }
      if (listener.current) {
        // @ts-ignore
        listener.current.off("speaking", onStartSpeaking);
        // @ts-ignore
        listener.current.off("stopped_speaking", onStopSpeaking);
      }
      if (stream.current) {
        stream.current.getTracks().forEach((track) => track.stop());
        stream.current = undefined;
      }
    };
  }, []);

  const onStartStreaming = async () => {
    try {
      if (stream.current) {
        stream.current.getTracks().forEach((track) => track.stop());
      }
      stream.current = await navigator.mediaDevices.getUserMedia({ audio: true });

      if (!listener.current) {
        const { default: hark } = await import("hark");
        listener.current = hark(stream.current, { interval: 100, play: false });
        listener.current.on("speaking", onStartSpeaking);
        listener.current.on("stopped_speaking", onStopSpeaking);
      }
    } catch (e) {
      console.error(e);
    }
  };
  const onStopStreaming = async () => {
    if (listener.current) {
      // @ts-ignore
      listener.current.off("speaking", onStartSpeaking);
      // @ts-ignore
      listener.current.off("stopped_speaking", onStopSpeaking);
      listener.current = undefined;
    }
    if (stream.current) {
      stream.current.getTracks().forEach((track) => track.stop());
      stream.current = undefined;
    }
  };

  const onStartRecording = async () => {
    try {
      if (!stream.current) {
        await onStartStreaming();
      }
      if (!stream.current) {
        console.error("Can not start streaming!");
        return;
      }
      if (!recorder.current) {
        const {
          default: { RecordRTCPromisesHandler, StereoAudioRecorder },
        } = await import("recordrtc");
        const recorderConfig: Options = {
          mimeType: "audio/wav",
          numberOfAudioChannels: 1,
          recorderType: StereoAudioRecorder,
          sampleRate: samplingRate,
          timeSlice: streaming ? timeSlice : undefined,
          type: "audio",
          ondataavailable: streaming ? onDataAvailable : undefined,
        };
        recorder.current = new RecordRTCPromisesHandler(stream.current, recorderConfig);
      }
      const recordState = await recorder.current.getState();
      if (recordState === "inactive" || recordState === "stopped") {
        await recorder.current.startRecording();
      }
      if (recordState === "paused") {
        await recorder.current.resumeRecording();
      }
      setRecording(true);
    } catch (e) {
      console.error(e);
    }
  };
  const onPauseRecording = async () => {
    if (!recorder.current) {
      return;
    }
    try {
      const recordState = await recorder.current.getState();
      if (recordState === "recording") {
        await recorder.current.pauseRecording();
      }
      setRecording(false);
    } catch (e) {
      console.error(e);
    }
  };
  const onStopRecording = async () => {
    if (!recorder.current) {
      return;
    }
    try {
      const recordState = await recorder.current.getState();
      if (recordState === "recording" || recordState === "paused") {
        await recorder.current.stopRecording();
      }
      onStopStreaming();
      setRecording(false);
      const blob = await recorder.current.getBlob();
      setBlob(blob);
      await recorder.current.destroy();
      chunks.current = [];
      recorder.current = undefined;
    } catch (e) {
      console.error(e);
    }
  };

  const onStartSpeaking = () => setSpeaking(true);
  const onStopSpeaking = () => setSpeaking(false);

  const onDataAvailable = async (data: Blob) => {
    if (!streaming || !recorder.current) {
      return;
    }
    try {
      onDataAvailableCallback?.(data);
      chunks.current.push(data);
    } catch (e) {
      console.error(e);
    }
  };

  const startRecording = onStartRecording;
  const pauseRecording = onPauseRecording;
  const stopRecording = onStopRecording;

  return {
    recording,
    speaking,
    blob,
    chunks: chunks.current,
    pauseRecording,
    startRecording,
    stopRecording,
  };
};

export type UseRTCConfig = {
  streaming?: boolean;
  timeSlice?: number;
  samplingRate?: number;
  onDataAvailable?: (blob: Blob) => void;
};

export type UseRTCReturn = {
  recording: boolean;
  speaking: boolean;
  blob?: Blob;
  chunks: Blob[];
  pauseRecording: () => Promise<void>;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<void>;
};

export type UseRTCHook = (config?: UseRTCConfig) => UseRTCReturn;
