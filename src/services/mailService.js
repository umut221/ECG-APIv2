const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth:{
        user:'xxxxx@gmail.com',
        pass: ""
    },
});

exports.sendMail = (to, subject, html) => {
    var mailOptions = {
        from: "xxxxx@gmail.com",
        to: to,
        subject: subject,
        html: html
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if(error)
            console.log(error);
        else
            console.log(`Email yollandı: ${info.response}`);
    });
};