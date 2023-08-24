export type MessageRole = "assistant" | "user" | "system" | "function";

export type Function = {
  name: string;
  description?: string;
  parameters: Record<string, any>;
};

export type Message = {
  role: MessageRole;
  content?: string;
  name?: string;
  function_call?: { name: string; arguments: string };

  // TODO: ..........
  plugin?: Plugin;
};

export type Chat = {
  id: string;
  title: string;
  model: string;
  createTime: Date;
  updateTime: Date;
  saved?: boolean;
};

export type Plugin = {
  name?: string;
  nameForHuman?: string;
  status?: "working" | "done";
  request?: any;
  response?: any;
};

export type Argument = { name: string; type: string; required?: boolean; description: string };

export class PluginAgent {
  name: string;
  nameForHuman?: string;
  description: string;
  arguments?: Argument[];

  constructor(name: string, desc: string, args?: Argument[], nameForHuman?: string) {
    this.name = name;
    this.description = desc;
    this.arguments = args;
    this.nameForHuman = nameForHuman;
  }

  async run(args: string) {
    const body = { name: this.name, args };
    const result = await fetch(`/api/v1/plugins/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return await result.json();
  }

  public toFunction = (): any => {
    const properties = {} as any;
    this.arguments?.forEach((arg) => {
      properties[arg.name] = { type: arg.type, description: arg.description };
    });
    const func = {
      name: this.name,
      description: this.description,
      parameters: {
        type: "object",
        required: this.arguments?.filter((arg) => arg.required).map((arg) => arg.name),
        properties,
      },
    };
    return func;
  };
}
