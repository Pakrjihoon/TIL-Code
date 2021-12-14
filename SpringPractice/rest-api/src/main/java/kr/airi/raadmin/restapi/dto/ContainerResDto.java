package kr.airi.raadmin.restapi.dto;

import kr.airi.raadmin.restapi.entity.Container;

import lombok.*;

@ToString
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ContainerResDto {

    private int number;
    private String container;
    private String content;
    private int serverNumber;
    private int portNumber;
    private ServerSpecReqDto serverSpecReqDto;

    public Container toEntity() {
        return Container.builder()
                .number(this.number)
                .container(this.container)
                .content(this.content)
                .serverNumber(this.serverNumber)
                .portNumber(this.portNumber)
                .build();
    }
}
