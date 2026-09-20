# ExamGuard - Testing Documentation

## 1. Testing Objective

Testing is performed to verify that the major ExamGuard modules operate as expected and that monitoring events are correctly recorded and processed.

## 2. Functional Test Cases

| Test ID | Test Case | Expected Result |

|---|---|---|

| TC01 | Open student portal | Student portal loads successfully |

| TC02 | Student authentication | Valid credentials allow access |

| TC03 | Invalid authentication | Invalid credentials are rejected |

| TC04 | Start examination | Examination interface opens |

| TC05 | Answer questions | Answers are recorded |

| TC06 | Submit examination | Examination submission is processed |

| TC07 | Webcam monitoring | Camera monitoring starts when configured |

| TC08 | Face detection | Face presence is detected |

| TC09 | Face absence | Face absence event is recorded |

| TC10 | Multiple faces | Multiple-face event is recorded |

| TC11 | Tab switch | Tab-switch event is recorded |

| TC12 | Focus loss | Focus-loss event is recorded |

| TC13 | Audio monitoring | Configured audio activity is detected |

| TC14 | Violation calculation | Event weights are processed |

| TC15 | Admin portal | Admin interface loads successfully |

| TC16 | Integrity analytics | Integrity information is displayed |

| TC17 | Report generation | Structured report is generated |

## 3. Computer Vision Testing

The face monitoring functionality should be tested under different conditions:

- Face visible to camera.

- Face temporarily outside camera view.

- More than one face visible.

- Different lighting conditions.

- Different camera positions.

## 4. Browser Monitoring Testing

Browser monitoring should be tested by:

- Switching away from the examination tab.

- Returning to the examination tab.

- Moving focus away from the examination window.

- Returning focus to the examination window.

## 5. Audio Monitoring Testing

Audio monitoring should be tested using different levels of environmental audio to verify that the configured detection mechanism records the intended events.

## 6. Integrity Testing

Integrity analysis should be tested by generating different combinations of monitoring events and verifying that the configured violation weights are applied.

Configured weights:

- Tab Switch: 8

- Focus Loss: 5

- Face Absent: 10

- Multiple Face: 15

- Audio Spike: 6

- Face Mismatch: 12

## 7. Admin Testing

Verify that an administrator can:

- Authenticate.

- Access the admin interface.

- View examination information.

- View monitoring events.

- View integrity information.

- Access analytics.

- Generate or review reports.

## 8. Cross-Platform Testing

The application should be tested in the environments available to the project team.

The repository provides dependency installation instructions so that another developer can create a platform-specific virtual environment.

## 9. Testing Result

The project is considered ready for demonstration when the major student, monitoring, integrity analysis, administrative, and reporting workflows operate without blocking errors.