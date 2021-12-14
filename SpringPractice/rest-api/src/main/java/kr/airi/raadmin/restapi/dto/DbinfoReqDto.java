package kr.airi.raadmin.restapi.dto;

import kr.airi.raadmin.restapi.entity.DbInfo;
import lombok.*;

@ToString
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class DbinfoReqDto {
    private int number;
    private String name;
    private String content;
    private int serverNumber;
    private String kind;

    public DbInfo toEntity() {
        return DbInfo.builder()
                .number(this.number)
                .name(this.name)
                .content(this.content)
                .serverNumber(this.serverNumber)
                .kind(this.kind)
                .build();
    }
}
