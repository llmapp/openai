import { crud, setHost } from "./crud";

import type { CrudItem } from "./crud/types";
import type { Message as Msg } from "../components/lib/chat/types";

setHost("/api");

export type RemoteChat = CrudItem & { title?: string; model: string };
export const chat = crud<RemoteChat>("chat");

export type RemoteMessage = CrudItem & { chat?: string; message: Msg };
export const message = (chat: string) => crud<RemoteMessage>("message", chat);
