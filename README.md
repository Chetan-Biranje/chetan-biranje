<p align="center"><img src="./cards/hero.svg" width="100%" alt="Chetan Biranje. Application security, web and API VAPT, DevSecOps."></p>

<p align="center"><img src="./cards/activity.svg" width="100%" alt="GitHub contribution graph"></p>

<p align="center"><img src="./cards/monthly.svg" width="100%" alt="Contributions by month with streaks"></p>

<p align="center">
<a href="https://github.com/Chetan-Biranje?tab=repositories"><img src="./cards/build.svg" width="32.5%" alt="Build"></a>
<a href="https://medium.com/@Chetan_Biranje"><img src="./cards/brand.svg" width="32.5%" alt="Brand"></a>
<a href="https://www.linkedin.com/in/chetanbiranje"><img src="./cards/learn.svg" width="32.5%" alt="Learn"></a>
</p>

<p align="center"><img src="./cards/skills.svg" width="100%" alt="Focus areas"></p>

<p align="center">
<a href="https://github.com/Chetan-Biranje/API-Authorization-Matrix-Automated-BOLA-BFLA-Detection"><img src="./cards/repo-1.svg" width="100%" alt="API-Authorization-Matrix-Automated-BOLA-BFLA-Detection"></a>
<a href="https://github.com/Chetan-Biranje/insider-threat-investigation-lab"><img src="./cards/repo-2.svg" width="100%" alt="insider-threat-investigation-lab"></a>
<a href="https://github.com/Chetan-Biranje/webapp-pentest-framework"><img src="./cards/repo-3.svg" width="100%" alt="webapp-pentest-framework"></a>
</p>

<p align="center"><a href="https://chetanbiranje.vercel.app">Portfolio</a> · <a href="https://www.linkedin.com/in/chetanbiranje">LinkedIn</a> · <a href="mailto:chetanbiranje@proton.me">Email</a></p>

## About

I am a BCA student in Pune working toward a career as a cybersecurity researcher. Before
this I completed a diploma in Electronics and Telecommunication and worked for four years
in sales and as a site supervisor. I study in the hours my job leaves free, and I keep what I
learn here as notes, labs and small tools.

My focus is web and API security, and I do bug bounty research on
[HackerOne](https://hackerone.com/chetanbiranje).

## How this profile grew

Dates are the first commit in each repository.

| When | What I did | Repositories |
|---|---|---|
| Before 2026 | Diploma in Electronics and Telecommunication. Four years in sales and site supervision | |
| Mar 2026 | First Java programs. Created this profile | [Java_Journey](https://github.com/Chetan-Biranje/Java_Journey) |
| Apr 2026 | Wrote study notes and labs: OWASP Top 10, threat modeling, secure coding, AppSec checklists, Linux post-exploitation, a web pentest methodology, REST API testing | [owasp-top10-lab-notes](https://github.com/Chetan-Biranje/owasp-top10-lab-notes), [threat-modeling-notes](https://github.com/Chetan-Biranje/threat-modeling-notes), [secure-coding-notes](https://github.com/Chetan-Biranje/secure-coding-notes), [appsec-checklists-playbooks](https://github.com/Chetan-Biranje/appsec-checklists-playbooks), [linux-post-exploitation-lab](https://github.com/Chetan-Biranje/linux-post-exploitation-lab), [webapp-pentest-framework](https://github.com/Chetan-Biranje/webapp-pentest-framework), [web-rest-api-pentest-research](https://github.com/Chetan-Biranje/web-rest-api-pentest-research) |
| Aug 2026 | Moved from notes to code: a security utilities library, a header and TLS checker, CI/CD examples | [python-security-utilities](https://github.com/Chetan-Biranje/python-security-utilities), [security-recon-toolkit](https://github.com/Chetan-Biranje/security-recon-toolkit), [devsecops-learning-lab](https://github.com/Chetan-Biranje/devsecops-learning-lab), [Secure-CI-CD-pipelines](https://github.com/Chetan-Biranje/Secure-CI-CD-pipelines) |
| Late Aug 2026 | Built a scanner that tests API authorization from a role matrix and detects BOLA and BFLA | [API-Authorization-Matrix-Automated-BOLA-BFLA-Detection](https://github.com/Chetan-Biranje/API-Authorization-Matrix-Automated-BOLA-BFLA-Detection) |
| Sep 2026 | Reusable CI workflow for secret, code and dependency scanning | [automatic-DevSecOps-security-workflow](https://github.com/Chetan-Biranje/automatic-DevSecOps-security-workflow) |
| Oct 2026 | Digital forensics lab that builds a timeline from USB, browser and file activity. CodeAlpha internship tasks | [insider-threat-investigation-lab](https://github.com/Chetan-Biranje/insider-threat-investigation-lab), [CodeAlpha_Phishing_Awareness](https://github.com/Chetan-Biranje/CodeAlpha_Phishing_Awareness), [CodeAlpha_Basic_Network_Sniffer](https://github.com/Chetan-Biranje/CodeAlpha_Basic_Network_Sniffer) |
| Oct to Nov 2026 | An n8n workflow project for my startup | [Startup](https://github.com/Chetan-Biranje/Startup) |

The early repositories are mostly notes. The later ones have code, tests and CI.

## Projects with results

* **API authorization scanner.** 3 roles, 3 endpoints, 10 generated cases. It found 0 issues
  in the secure app and all 3 seeded flaws (1 BOLA, 2 BFLA) in the vulnerable mode. The
  sample is small, so this shows that the method works, not how accurate it is. Along the way
  the first version mislabeled BOLA as BFLA. I found it, fixed it and added tests.
* **Python security utilities.** Encryption, password hashing, a JWT validator, a rate limiter
  and more, with 18 tests. It has not been independently reviewed.
* **Insider threat lab.** A command-line tool and dashboard that turn exported logs into a
  timeline and flag leads for an investigator. It uses synthetic data and 4 tests.

## Next

* Extend the authorization scanner to POST, PUT and DELETE endpoints and read OpenAPI files
* Finish BCA

