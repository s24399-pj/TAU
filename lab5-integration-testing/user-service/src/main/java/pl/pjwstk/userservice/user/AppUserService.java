package pl.pjwstk.userservice.user;

import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import pl.pjwstk.userservice.user.command.CreateAppUserCommand;
import pl.pjwstk.userservice.user.command.UpdateAppUserCommand;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AppUserService {
    private final AppUserRepository appUserRepository;

    @Transactional(readOnly = true)
    public List<AppUser> findAll() {
        return appUserRepository.findAll();
    }

    @Transactional(readOnly = true)
    public AppUser findById(Long id) {
        return appUserRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("User not found with ID: " + id));
    }

    @Transactional
    public AppUser save(CreateAppUserCommand command) {
        return appUserRepository.save(AppUser.builder()
                .name(command.getName())
                .email(command.getEmail())
                .build());
    }

    @Transactional
    public AppUser update(UpdateAppUserCommand command) {
        AppUser existingUser = appUserRepository.findById(command.getAppUserId())
                .orElseThrow(() -> new EntityNotFoundException("User not found with ID: " + command.getAppUserId()));

        existingUser.setName(command.getName());
        existingUser.setEmail(command.getEmail());
        return appUserRepository.saveAndFlush(existingUser);
    }

    @SneakyThrows
    public void delete(Long id) {
        if (!appUserRepository.existsById(id)) {
            throw new EntityNotFoundException("User not found with ID: " + id);
        }
        appUserRepository.deleteById(id);
    }
}
