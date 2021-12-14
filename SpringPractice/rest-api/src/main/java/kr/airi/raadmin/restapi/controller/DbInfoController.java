package kr.airi.raadmin.restapi.controller;

import kr.airi.raadmin.restapi.dto.DbinfoReqDto;
import kr.airi.raadmin.restapi.entity.DbInfo;
import kr.airi.raadmin.restapi.service.DbInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin
@RequestMapping(value = "/api")
public class DbInfoController {

    private DbInfoService dbInfoService;

    @Autowired
    DbInfoController(DbInfoService dbInfoService) {
        this.dbInfoService = dbInfoService;
    }

    @GetMapping(value = "/dbinfos")
    @ResponseBody
    public List<DbInfo> getAllDbInfo() {
        return dbInfoService.getAll();
    }

    @PostMapping(value = "/dbinfo")
    @ResponseBody
    public DbInfo saveDbInfo(@RequestBody DbinfoReqDto req) {
        return dbInfoService.createOne(req);
    }

    @GetMapping(value = "/dbinfo/{number}")
    public DbInfo getDbinfo(@PathVariable("number")int number){
        return dbInfoService.getOne(number);
    }
}
