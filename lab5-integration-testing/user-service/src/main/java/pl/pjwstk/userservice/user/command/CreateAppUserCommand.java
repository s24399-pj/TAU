package pl.pjwstk.userservice.user.command;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.FieldDefaults;

@Getter
@Setter
@FieldDefaults(level = AccessLevel.PRIVATE)
public class CreateAppUserCommand {

    @NotBlank(message = "NAME_NOT_NULL")
    @Size(min = 5, max = 100, message = "NAME_WRONG_SIZE")
    String name;

    @NotBlank(message = "EMAIL_NOT_NULL")
    @Email(message = "EMAIL_NOT_VALID")
    @Size(min = 5, max = 150, message = "EMAIL_WRONG_SIZE")
    String email;

}
