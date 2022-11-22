# Nezrena Mail Module

Joined IMAP/SMTP client for sending and receiving emails and their attachements.

## Setup

1. Install NodeJS dependencies with `npm install`

2. Create `config.json` with this content
```JSON
{
  "imap": {
    "user": "changeme@example.com",
    "password": "changeme",
    "host": "imap.gmail.com",
    "port": 993,
    "tls": true
  },
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 465,
    "secure": true,
    "auth": {
      "user": "changeme@example.com",
      "pass": "changeme"
    }
  }
}
```

3. Now your module is ready to work.

## Usage

### Downloading emails

1. Run module without arguments.
This will download all emails from mailbox provided in `config.json` and save them to `mail/in` folder.

### Sending emails

1. Add `to` field to `mail.json` of specific email.
2. Move whole folder to `mail/out`.
3. Run module with email ID (folder name).
This will send provided email and move its folder to `mail/sent` folder.