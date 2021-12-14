package kr.airi.raadmin.restapi.dto;

import kr.airi.raadmin.restapi.entity.ServerSpec;
import lombok.*;

import javax.persistence.Column;

@ToString
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ServerSpecReqDto {
    private int serverNumber;

    private String host;
    private String hostName;
    private int cpuCore;
    private String gpu;
    private String ram;
    private String disk;
    private String manager;

    public ServerSpec toEntity() {
        return ServerSpec.builder()
                .serverNumber(this.serverNumber)
                .host(this.host)
                .hostName(this.hostName)
                .cpuCore(this.cpuCore)
                .gpu(this.gpu)
                .ram(this.ram)
                .disk(this.disk)
                .manager(this.manager)
                .build();
    }

}
