package pl.pjwstk.userservice.user;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import pl.pjwstk.userservice.user.command.CreateAppUserCommand;
import pl.pjwstk.userservice.user.command.UpdateAppUserCommand;

import java.util.List;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class AppUserController {

    private final AppUserService appUserService;

    @GetMapping
    public List<AppUser> findAllUsers() {
        return appUserService.findAll();
    }

    @GetMapping("/{id}")
    public AppUser findUserById(@PathVariable Long id) {
        return appUserService.findById(id);
    }

    @PostMapping
    @ResponseStatus(value = HttpStatus.CREATED)
    public AppUser createUser(@RequestBody @Valid CreateAppUserCommand command) {
        return appUserService.save(command);
    }

    @PutMapping
    public AppUser updateUser(@RequestBody @Valid UpdateAppUserCommand command) {
        return appUserService.update(command);
    }

    @DeleteMapping("/{id}")
    public void deleteUserById(@PathVariable Long id) {
        appUserService.delete(id);
    }


}
