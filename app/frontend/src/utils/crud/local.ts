import { nanoid } from "nanoid";

import { CrudApi, CrudItem } from "./types";

export const setHost = (host: string) => {};

export const crud = <T extends CrudItem>(type: string, belongTo?: string): CrudApi<T> => {
  const calcId = (id: string) => (belongTo ? [belongTo, id].join("-") : id);

  return {
    create: async (item: T) => {
      if (item.id === undefined) {
        item.id = nanoid(10);
      }
      const saved = store.save<T>(item, calcId(item.id), type);
      return saved ? item.id : undefined;
    },
    get: async (id: string) => {
      const thisId = calcId(id);
      return store.get<T>(thisId, type);
    },
    query: async (params?: { [key: string]: string }, order?: "asc" | "dsc"): Promise<T[]> => {
      const json = store.query<T>(type, belongTo);
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
      const newItem: T = values ? { ...item, ...values } : item;
      const updated = store.update<T>(newItem, calcId(newItem.id ?? ""), type);
      return !!updated;
    },
    delete: async (id: string, childType?: string) => {
      store.delete(id, type);
      console.log("delete", id, childType);
      if (childType) {
        const childItems = store.query<CrudItem>(childType, id);
        childItems.forEach((c) => store.delete(id + "-" + c.id, childType));
      }
      return true;
    },
  };
};

export const store = {
  query: <T>(type: string, belongTo?: string) => {
    const prefix = belongTo ? `${type}-${belongTo}` : type;
    const result = Object.keys(localStorage)
      .filter((k) => k.startsWith(`${prefix}-`))
      .map((k) => localStorage.getItem(k))
      .filter((c) => c !== null)
      .map((c) => JSON.parse(c || "{}") as T);
    return result;
  },
  get: <T>(key: string, type: string) => {
    const data = localStorage.getItem(`${type}-${key}`);

    if (data) {
      return JSON.parse(data) as T;
    }
    return undefined;
  },
  save: <T>(item: T, key: string, type: string) => {
    localStorage.setItem(`${type}-${key}`, JSON.stringify(item));
    return item;
  },
  update: <T>(item: T, key: string, type: string) => {
    localStorage.setItem(`${type}-${key}`, JSON.stringify(item));
    return item;
  },
  delete: (key: string, type: string) => {
    localStorage.removeItem(`${type}-${key}`);
  },
};
