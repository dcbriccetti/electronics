<html>
  <head>
    <title>WebSwitch</title>
    <style type="text/css">
    a {
        text-color: blue;
        font-family: monospace;
        color: black;
        border-radius: 6px;
    }
    #buttons {
        background-color: grey;
    }
    </style>
  </head>
        
<body>
<h1>Web Switch</h1>
<p>Hey, guess what? You can control LEDs from here!</p>
<div id="buttons">
<a href="/on"><button id="a">Turn on red</button></a>
<a href="/off"><button id="a">Turn off red</button></a>
<a href="/blinkblue"><button id="a">Blink blue</button></a>
<a href="/blinkboth"><button id="a">Blink red and blue alternately</button></a>
<a href="/blinktogether"><button id="a">Blink red and blue together</button></a>
<a href="/blinkall"><button id="a">Blink red, blue, and green in sequence</button></a>
<a href="/show7"><button id="a">Show 7 colors in sequence</button></a>
<a href="/random"><button id="a">Show random colors</button></a>
<a href="/snazzyblink"><button id="a">Snazzy Blink</button></a>
</div>
</body>
</html>
