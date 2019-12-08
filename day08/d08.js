var fs = require('fs');
fs.readFile('d08.in', 'utf8', function(err, data) {
    solve08(data);
});

const M = 25;
const N = 6;

/**
 * @param {string} data
 */
function solve08(data) {
  var numLayers = data.length / (M*N);
  var maxLayer = 0;
  var minZeros = M*N;
  var layers = [];
  for (let i = 0; i < numLayers; i++) {
    layers.push(data.slice(i*M*N, (i+1)*M*N));
    var zeros = layers[layers.length - 1].split('0').length - 1;
    if (zeros < minZeros) {
      maxLayer = i;
      minZeros = zeros;
    }
  }

  var result = (layers[maxLayer].split('1').length - 1) * (layers[maxLayer].split('2').length - 1);
  console.log('Part 1:', result);

  var image = [];
  for (let i = 0; i < M*N; i++) {
    var color = '2';
    for (let j = 0; j < numLayers; j++) {
      if (layers[j][i] != '2') {
        color = layers[j][i];
        break;
      }
    }
    image.push(color);
  }

  printImage(image);
}

/**
 *
 * @param {array} image
 */
function printImage(image) {
  console.log('Part 2:')
  for (let i = 0; i < N; i++) {
    console.log(image.slice(i*M, (i+1)*M).join(''))
  }
}