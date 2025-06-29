package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;

@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
        try {
            JAXBContext context = JAXBContext.newInstance(String.class);
        } catch (JAXBException e) {
            e.printStackTrace();
        }
    }
}
