const express = require('express');
const path = require('path')
const app = new express();

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.set('views', path.join(__dirname));

app.get('/', function(req, res){
    res.contentType('text/html')
    res.render('template')
}).listen(8080);