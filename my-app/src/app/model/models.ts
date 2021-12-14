export interface ServerItem {
    serverNumber: number;
    host: String;
    hostName: String;
    cpuCore: number;
    gpu: String;
    ram: String;
    disk: String;
    manager: String;
}
export interface ContainerItem {
    number: number;
    container: String;
    content: String;
    serverNumber : number;
    portNumber: number;
    serverSpec: ServerItem;
}

