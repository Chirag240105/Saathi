export const qk = {
  status: ["status"] as const,
  toolCalls: ["tool-calls"] as const,
  events: (type: string) => ["events", type] as const,
  history: (days: number) => ["history", days] as const,
  list: (resource: string) => [resource] as const,
};
