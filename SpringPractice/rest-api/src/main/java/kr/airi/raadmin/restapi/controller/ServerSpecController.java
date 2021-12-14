package kr.airi.raadmin.restapi.controller;

import kr.airi.raadmin.restapi.dto.ServerSpecReqDto;
import kr.airi.raadmin.restapi.entity.ServerSpec;
import kr.airi.raadmin.restapi.repository.ServerSpecRepository;
import kr.airi.raadmin.restapi.service.ServerSpecService;
import org.apache.catalina.util.ServerInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin
@RequestMapping(value = "/api")
public class ServerSpecController {

    private ServerSpecService serverSpecService;

    @Autowired
    ServerSpecController(ServerSpecService serverSpecService) {
        this.serverSpecService = serverSpecService;
    }

    @GetMapping(value = "/server-spec")
    @ResponseBody
    public List<ServerSpec> getAllServerSpec() {
        return serverSpecService.getAll();
    }

    @PostMapping(value = "/server-spec")
    public ServerSpec saveServerSpec(@RequestBody ServerSpecReqDto req) {
        return serverSpecService.createOne(req);
    }

    @GetMapping(value = "/server-spec/{number}")
    public ServerSpec getServerSpec(@PathVariable("number")int number) {
        return serverSpecService.getOne(number);
    }
}
