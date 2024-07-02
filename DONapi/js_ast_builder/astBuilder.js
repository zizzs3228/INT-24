const fs = require('fs');
const path = require('path');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;

// Рекурсивная функция для удаления свойств loc, start и end из AST
function removeLoc(node) {
  if (typeof node !== 'object' || node === null) {
    return;
  }
  
  delete node.loc;
  delete node.start;
  delete node.end;
  delete node.extra
  
  for (const key in node) {
    if (node.hasOwnProperty(key)) {
      removeLoc(node[key]);
    }
  }
}

// Читаем исходный код из файла
const code = fs.readFileSync(path.resolve(__dirname, 'temp/code.js'), 'utf-8');

// Парсим код
const ast = parser.parse(code, {
  sourceType: 'module',
  plugins: [
    'jsx',
    'typescript',
    'classProperties',
    'decorators-legacy',
  ],
  ranges: false,
  tokens: false,
  loc: false,
  comments: false,
  extra: false
});

removeLoc(ast);
const json_ast = JSON.stringify(ast, null, 2);
console.log(json_ast);

const generatedCode = generator(ast).code;

console.log(generatedCode)

// Записываем сгенерированный код в файл
fs.writeFile('generatedAST.json', json_ast, err => {
  if (err) {
    console.error(err);
  } else {
    console.log('Generated code has been written to generatedCode.js');
  }
});