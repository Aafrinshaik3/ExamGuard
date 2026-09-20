# ExamGuard - User Stories

## US01 - Student Authentication

**As a student, I want to authenticate into ExamGuard so that I can access my examination securely.**

### Acceptance Criteria

- Student can provide authentication credentials.

- Valid credentials allow access.

- Invalid credentials are rejected.

- Student is directed to the appropriate examination interface.

---

## US02 - Administrator Authentication

**As an administrator, I want to access the administrator interface so that I can review examination information.**

### Acceptance Criteria

- Administrator can authenticate.

- Administrator can access administrative functionality.

- Student functionality is separated from administrator functionality.

---

## US03 - Online Examination

**As a student, I want to take an online examination so that I can complete my assessment remotely.**

### Acceptance Criteria

- Student can access the examination.

- Questions are displayed.

- Student can provide answers.

- Student can submit the examination.

---

## US04 - Face Monitoring

**As an administrator, I want ExamGuard to monitor face presence so that examination-related face events can be recorded.**

### Acceptance Criteria

- Webcam monitoring can be initiated.

- Face presence can be detected.

- Face absence can be identified.

- Monitoring events can be recorded.

---

## US05 - Multiple Face Detection

**As an administrator, I want the system to detect multiple faces so that the presence of additional people can be recorded as a monitoring event.**

### Acceptance Criteria

- Camera frames are analyzed.

- Multiple detected faces are identified.

- A monitoring event is generated.

---

## US06 - Browser Monitoring

**As an administrator, I want tab switching and focus-loss events to be monitored so that examination browser activity can be recorded.**

### Acceptance Criteria

- Tab switching is detected.

- Focus loss is detected.

- Events are recorded for integrity analysis.

---

## US07 - Audio Monitoring

**As an administrator, I want configured audio activity to be monitored so that unusual audio events can contribute to examination analysis.**

### Acceptance Criteria

- Audio monitoring is available when configured.

- Audio activity is processed.

- Configured audio-spike events are recorded.

---

## US08 - Integrity Analysis

**As an administrator, I want monitoring events to contribute weighted violation points so that examination integrity can be analyzed systematically.**

### Acceptance Criteria

- Each configured event has an associated weight.

- Detected events contribute to the violation analysis.

- The accumulated information is available for administrative review.

---

## US09 - Admin Analytics

**As an administrator, I want to review examination monitoring and integrity information so that I can understand the activity recorded during an examination.**

### Acceptance Criteria

- Administrator can view examination information.

- Administrator can review violations.

- Administrator can review integrity information.

- Analytics are available through the configured interface.

---

## US10 - Report Generation

**As an administrator, I want a structured examination integrity report so that monitoring information can be reviewed in a readable format.**

### Acceptance Criteria

- Examination information is collected.

- Monitoring information is processed.

- A structured narrative report can be generated.