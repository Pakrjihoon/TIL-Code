package kr.airi.raadmin.restapi.controller;

import kr.airi.raadmin.restapi.dto.ContainerReqDto;
import kr.airi.raadmin.restapi.dto.ContainerUdtDto;
import kr.airi.raadmin.restapi.entity.Container;
import kr.airi.raadmin.restapi.service.ContainerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@CrossOrigin
@RequestMapping("/api")
public class ContainerController {

    private ContainerService containerService;

    @Autowired
    ContainerController(ContainerService containerService) {
        this.containerService = containerService;
    }

    @GetMapping(value = "/containers")
    @ResponseBody
    public List<Container> getAllContainer() {
        return containerService.getAll();
    }

    @PostMapping(value = "/container")
    @ResponseBody
    public Container saveContainer(@RequestBody ContainerReqDto req) {
        return containerService.createOne(req);
    }

    @GetMapping(value = "/container/{number}")
    @ResponseBody
    public Container getContainer(@PathVariable("number")int number){
        return containerService.getOne(number);
    }

    @PutMapping(value = "/container/{number}")
    @ResponseBody
    public Optional<Container> updateContainer(@PathVariable ("number")int number, @RequestBody ContainerUdtDto containerUdtDto) {
        return containerService.update(number, containerUdtDto);
    }

    @DeleteMapping(value = "/container/{number}")
    @ResponseBody
    public void deleteContainer(@PathVariable("number")int number){
        containerService.delete(number);
    }
}
