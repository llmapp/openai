import { CrudApi, CrudItem } from "./types";

const config = { host: "/api" };

export const setHost = (host: string) => {
  config.host = host;
};

export const crud = <T extends CrudItem>(type: string, belongTo?: string, belongToType?: string): CrudApi<T> => {
  const endpoint = "/api/chats/" + belongTo + "/messages";
  return {
    create: async (item: T): Promise<string | undefined> => {
      const url = getUrl(type, endpoint);
      return await request.post(url, item);
    },
    get: async (id: string): Promise<T | undefined> => {
      const url = getUrl(type, endpoint, id);
      const json = await request.get(url);
      return json as T;
    },
    query: async (params?: { [key: string]: string }, order?: "asc" | "dsc"): Promise<T[]> => {
      const paramsStr = Object.keys(params ?? {})
        .map((key) => `${key}=${params?.[key]}`)
        .join("&");
      const base = getUrl(type, endpoint);
      const url = params ? `${base}?${paramsStr}` : base;
      const json = (await request.get(url)) as T[];

      if (!order) {
        return json;
      }
      if (order === "asc") {
        return json.sort((a, b) => new Date(b.updateTime).getTime() - new Date(a.updateTime).getTime());
      } else {
        return json.sort((a, b) => new Date(a.updateTime).getTime() - new Date(b.updateTime).getTime());
      }
    },
    update: async (item: T, values?: { [key: string]: any }) => {
      item.updateTime = new Date();
      if (!item.createTime) {
        item.createTime = new Date();
      }
      const newItem: T = values ? { ...item, ...values } : item;

      const url = getUrl(type, endpoint);
      return request.put(url, newItem);
    },
    delete: async (id: string) => {
      const url = getUrl(type, endpoint);
      return request.delete(url, id);
    },
  };
};

const request = {
  post: async <T>(url: string, item: T) => {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(item),
    });
    return resp.ok ? await resp.json() : undefined;
  },
  get: async (url: string) => {
    const resp = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    return resp.ok ? await resp.json() : undefined;
  },
  put: async <T>(url: string, item: T) => {
    const resp = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(item),
    });
    return resp.ok;
  },
  delete: async (url: string, id: string) => {
    const resp = await fetch(`${url}/${id}`, { method: "DELETE" });
    return resp.ok;
  },
};

const getUrl = (type: string, endpoint?: string, id?: string) => {
  const resources = endpoint ?? `${config.host}/${type}s`;
  return id !== undefined ? `${resources}/${id}` : resources;
};
