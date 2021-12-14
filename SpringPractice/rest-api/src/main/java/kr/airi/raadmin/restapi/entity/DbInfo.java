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
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "server_dbinfo")
public class DbInfo {
    @Id
    private int number;

    private String name;
    private String content;

    @Column(name = "server_number")
    private int serverNumber;

    private String kind;

}
