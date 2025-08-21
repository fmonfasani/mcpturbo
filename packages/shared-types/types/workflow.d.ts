import { Message } from './message';

export interface Task {
  id: string;
  messages: Message[];
}

export interface Workflow {
  id: string;
  tasks: Task[];
}
