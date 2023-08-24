export type CrudItem = {
  id?: string;
  createTime: Date;
  updateTime: Date;
};

export type CrudApi<T> = {
  create: (item: T) => Promise<string | undefined>;
  query: (params?: { [key: string]: any }, order?: "asc" | "dsc") => Promise<T[] | undefined>;
  get: (id: string) => Promise<T | undefined>;
  update: (item: T) => Promise<boolean>;
  delete: (ids: string, childType?: string) => Promise<boolean>;
};
