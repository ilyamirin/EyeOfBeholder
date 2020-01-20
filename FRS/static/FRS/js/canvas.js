let canvas = document.getElementById('canvas');
let context = canvas.getContext('2d');

let frameLoop = null;
let firstWhite = false;
let old;

let canvasData = {
    "face": [],
    "coin": [],
};

function drawRect(rect, text, colorStroke, fillStyle){
    if ((rect[3] - rect[1]) * (rect[2] - rect[0]) > 900 * 675 / 3){
        return;
    }
    if (rect[2] > 650) rect[2] = 650;
    if (rect[3] > 890) rect[3] = 890;
    if (rect[1] < 10) rect[1] = 10;


    context.beginPath();
    context.rect(rect[1], rect[0], rect[3] - rect[1], rect[2] - rect[0]);

    context.strokeStyle = colorStroke;
    context.lineWidth = "3";
    context.stroke();
    context.closePath();

    context.beginPath();
    context.fillStyle = fillStyle;
    if (text.length * 9 + 10 >= rect[3] - rect[1] + 4)
        context.fillRect(rect[1] - 2 - (text.length * 9 + 8 - (rect[3] - rect[1])) / 2, rect[0] + rect[2] - rect[0], Math.max(rect[3] - rect[1] + 4, text.length * 9 + 10), 20);
    else
        context.fillRect(rect[1] - 2, rect[0] + rect[2] - rect[0], Math.max(rect[3] - rect[1] + 6, text.length * 9 + 10), 20);
    context.closePath();

    context.beginPath();
    context.font = "16px Arial";
    context.fillStyle = '#0067b1';
    if (text.length * 9 + 10 >= rect[3] - rect[1] + 4)
        context.fillText(text, rect[1] + 2 - (text.length * 9 + 10 - (rect[3] - rect[1])) / 2, rect[2] - rect[0] + rect[0] + 15);
    else
        context.fillText(text, rect[1] + 2, rect[2] - rect[0] + rect[0] + 15);
    context.closePath();
}

function drawCanvasData() {
    let userColor = 'blue';
    context.clearRect(0, 0, canvas.width, canvas.height);
    canvasData["face"].forEach((rect, i) =>
        drawRect(rect, rect[4],
            (!i && firstWhite) ? userColor: 'white', (!i && firstWhite) ?userColor : 'white'));
    canvasData["coin"].forEach(d => drawRect(d.coords, d.short_name, 'blue', 'blue'));
}

drawInterval = setInterval(() => drawCanvasData(), 1000 / 24);

function resetCanvas() {
    clearInterval(drawInterval);
    context.clearRect(0, 0, canvas.width, canvas.height);
}

function activateCanvas() {
    drawInterval = setInterval(() => drawCanvasData(), 1000 / 24);
}