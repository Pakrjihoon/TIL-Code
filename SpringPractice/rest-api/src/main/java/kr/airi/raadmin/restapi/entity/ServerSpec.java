package kr.airi.raadmin.restapi.entity;

import lombok.*;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Builder
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "server_spec")
public class ServerSpec {

    @Id
    @Column(name = "server_number")
    private int serverNumber;

    private String host;

    @Column(name = "host_name")
    private String hostName;

    @Column(name = "cpu_core")
    private int cpuCore;

    private String gpu;
    private String ram;
    private String disk;
    private String manager;

}
