//
// Nezrena Mail - Main module
// Illia Yavdoshchuk (c) 2022
//

const config = require("./config");
config.load();

const fs = require("fs");
const homepath = require("./homepath")

const args = process.argv.slice(2);
if (args.length > 0) {
    const nodemailer = require('nodemailer');

    try {
        fs.mkdirSync(homepath("mail/out/"));
    } catch (error) { }

    try {
        fs.mkdirSync(homepath("mail/sent/"));
    } catch (error) { }

    let file = args[0];

    if (fs.existsSync(homepath(`mail/out/${file}`)))
        fs.readFile(homepath(`mail/out/${file}/mail.json`), (err, data) => {
            if (err) {
                fs.renameSync(homepath(`mail/out/${file}`), homepath(`mail/sent/${file}`));
                return;
            }

            let mail = JSON.parse(data.toString());
            let files = fs.readdirSync(homepath(`mail/out/${file}`));

            const index = files.indexOf(homepath("mail.json"));
            if (index > -1)
                files.splice(index, 1);

            files = files.map(name => {
                return {
                    filename: name,
                    content: fs.readFileSync(homepath(`mail/out/${file}/${name}`))
                }
            });

            let transporter = nodemailer.createTransport(config.smtp);
            transporter.sendMail({
                from: mail.from,
                to: mail.to,
                subject: mail.subject,
                text: mail.message,
                html: mail.messageHtml,
                attachments: files
            });
            transporter.close();

            fs.renameSync(homepath(`mail/out/${file}`), homepath(`mail/sent/${file}`));
        });
}
else {
    const Imap = require('node-imap');
    const { simpleParser } = require('mailparser')

    try {
        fs.mkdirSync(homepath("mail/in/"));
    } catch (error) { }

    const imap = new Imap(config.imap);
    imap.once('ready', function () {
        imap.openBox('INBOX', function (err, box) {
            if (err)
                throw err;

            let msgs = box.messages.total;
            if (msgs == 0)
                imap.end();

            const fetchResult = imap.seq.fetch("1:" + msgs, { bodies: '' });

            fetchResult.on('message', function (msg, seqno) {
                let parser, uid
                msg.on('body', function (stream) {
                    parser = simpleParser(stream)
                });

                msg.once('attributes', function (attrs) {
                    uid = attrs.uid
                    console.log(uid + " Flags: " + attrs.flags.join(","))
                });

                msg.once('end', function () {
                    console.log(uid + ' Finished')
                    parser.then(parsed => {
                        const fromEmail = parsed.from?.value?.[0]?.address

                        if (fromEmail) {
                            try {
                                fs.mkdirSync(homepath(`mail/in/${uid}`));
                            } catch (error) { }

                            let mail = JSON.stringify({
                                from: parsed.from.text,
                                subject: parsed.subject,
                                date: parsed.date,
                                messageHtml: parsed.html ? parsed.html : undefined,
                                message: parsed.text
                            }, null, 4);

                            fs.writeFileSync(homepath(`mail/in/${uid}/mail.json`, mail));

                            for (let att of parsed.attachments)
                                fs.writeFile(homepath("mail/in/" + uid + "/" + att.filename), att.content, () => { });

                            imap.expunge(uid, () => {})
                            console.log(uid + ' Deleted')

                            if (--msgs == 0) {
                                imap.closeBox(true, (err) => { });
                                imap.end();
                            }
                        } else {
                            console.warn('No from email found in', parsed)
                        }
                    });
                });
            });

            fetchResult.once('end', function () {
                console.log('Done fetching all messages!');
            });
        });
    });

    imap.once('error', function (err) {
        console.log(err);
    });

    imap.once('end', function () {
        console.log('Connection ended');
    });

    imap.connect();
}
