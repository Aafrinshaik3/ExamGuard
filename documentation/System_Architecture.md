# ExamGuard - System Architecture

## 1. Architecture Overview

ExamGuard follows a modular web application architecture consisting of the student interface, administrator interface, backend application, monitoring components, database layer, and integrity analytics.

## 2. High-Level Architecture

```text
                    ExamGuard
                       |
        +--------------+--------------+
        |                             |
   Student Portal                Admin Portal
        |                             |
        +--------------+--------------+
                       |
                  Flask Backend
                       |
       +---------------+---------------+
       |               |               |
 Examination       Monitoring      Authentication
   Module            Module           & Roles
                       |
          +------------+------------+
          |            |            |
       OpenCV      Browser       Audio
       Camera      Events       Monitoring
          |            |            |
          +------------+------------+
                       |
                Violation Records
                       |
                Integrity Analysis
                       |
              +--------+--------+
              |                 |
        Integrity Score     Analytics
              |                 |
              +--------+--------+
                       |
                 Admin Review
                       |
               Narrative Report