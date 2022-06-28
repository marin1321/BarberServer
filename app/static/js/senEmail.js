const sendEmailContact = (e) =>{ 
    e.preventDefault()
    const user = document.getElementById("firstname").value;
    const emails = document.getElementById("Email").value;
	const numeroT = document.getElementById("phone").value;
    const messages = document.getElementById("message").value;
    messages = "Este fue tu mensaje: " + messages;
    var mandrill = require('node-mandrill')('6c2491c263b54d515bbbb484ce70e42f-us11');
    mandrill('/messages/send', {
        message: {
            to: [{email: emails, name: user}],
            from_email: 'barberserver1234company@gmail.com',
            subject: "Tu Mensaje Se ha enviado",
            text: messages
        }
    }, function(error, response)
    {
        //uh oh, there was an error
        if (error) console.log( JSON.stringify(error) );
        //everything's good, lets see what mandrill said
        else console.log(response);
    });

}
