package kr.airi.raadmin.restapi.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Getter
@ToString
@NoArgsConstructor
public class ContainerUdtDto {

    private String container;
    private String content;
    private int serverNumber;
    private int portNumber;
}
