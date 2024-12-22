package pl.pjwstk.userservice.user;


import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;
import pl.pjwstk.userservice.user.command.CreateAppUserCommand;
import pl.pjwstk.userservice.user.command.UpdateAppUserCommand;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;


@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class AppUserControllerTest {

    private static final String APPUSER_API = "/api/v1/users";

    @Autowired
    private ObjectMapper mapper;

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private AppUserRepository appUserRepository;

    @AfterEach
    public void cleanUp() {
        appUserRepository.deleteAll();
        appUserRepository.flush();
    }

    @Test
    @SneakyThrows
    void shouldFindAllUsers() {
        appUserRepository.save(AppUser.builder()
                .email("jan@pawel.drugi")
                .name("Juan Pablo")
                .build());

        mockMvc.perform(get(APPUSER_API))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", notNullValue()))
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].name", equalTo("Juan Pablo")))
                .andExpect(jsonPath("$[0].email", equalTo("jan@pawel.drugi")));
    }

    @Test
    @SneakyThrows
    void shouldFindCertainUser() {
        appUserRepository.save(AppUser.builder()
                .email("jan@pawel.drugi")
                .name("Juan Pablo")
                .build());

        mockMvc.perform(get(APPUSER_API + "/2"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", notNullValue()))
                .andExpect(jsonPath("$.name", equalTo("Juan Pablo")))
                .andExpect(jsonPath("$.email", equalTo("jan@pawel.drugi")));
    }

    @Test
    @SneakyThrows
    void shouldNotFindCertainUser() {
        mockMvc.perform(get(APPUSER_API + "/1"))
                .andExpect(status().is4xxClientError());
    }

    @Test
    @SneakyThrows
    void shouldCreateUser() {
        CreateAppUserCommand command = new CreateAppUserCommand();
        command.setName("John Doe");
        command.setEmail("john.doe@example.com");

        mockMvc.perform(post(APPUSER_API)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(command)))
                .andDo(print())
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name", equalTo("John Doe")))
                .andExpect(jsonPath("$.email", equalTo("john.doe@example.com")));
    }

    @Test
    @SneakyThrows
    void shouldFailToCreateUserWithInvalidData() {
        CreateAppUserCommand command = new CreateAppUserCommand();
        command.setName(""); // Invalid name
        command.setEmail("invalid-email"); // Invalid email

        mockMvc.perform(post(APPUSER_API)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(command)))
                .andDo(print())
                .andExpect(status().isBadRequest());
    }

    @Test
    @SneakyThrows
    void shouldUpdateUser() {
        AppUser existingUser = appUserRepository.save(AppUser.builder()
                .name("Jane Doe")
                .email("jane.doe@example.com")
                .build());

        UpdateAppUserCommand command = new UpdateAppUserCommand();
        command.setAppUserId(existingUser.getId());
        command.setName("Jane Smith");
        command.setEmail("jane.smith@example.com");

        mockMvc.perform(put(APPUSER_API)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(command)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name", equalTo("Jane Smith")))
                .andExpect(jsonPath("$.email", equalTo("jane.smith@example.com")));

        mockMvc.perform(get(APPUSER_API + "/" + existingUser.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name", equalTo("Jane Smith")))
                .andExpect(jsonPath("$.email", equalTo("jane.smith@example.com")));
    }

    @Test
    @SneakyThrows
    void shouldFailToUpdateNonExistingUser() {
        UpdateAppUserCommand command = new UpdateAppUserCommand();
        command.setAppUserId(999L);
        command.setName("Non Existing");
        command.setEmail("non.existing@example.com");

        mockMvc.perform(put(APPUSER_API)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(mapper.writeValueAsString(command)))
                .andDo(print())
                .andExpect(status().isNotFound());
    }

    @Test
    @SneakyThrows
    void shouldDeleteUser() {
        AppUser existingUser = appUserRepository.save(AppUser.builder()
                .name("John Doe")
                .email("john.doe@example.com")
                .build());

        mockMvc.perform(delete(APPUSER_API + "/" + existingUser.getId()))
                .andDo(print())
                .andExpect(status().isOk());

        mockMvc.perform(get(APPUSER_API + "/" + existingUser.getId()))
                .andExpect(status().isNotFound());
    }

    @Test
    @SneakyThrows
    void shouldFailToDeleteNonExistingUser() {
        mockMvc.perform(delete(APPUSER_API + "/3429412"))
                .andDo(print())
                .andExpect(status().isNotFound());
    }


}
