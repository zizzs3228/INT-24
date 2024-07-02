// server.js
const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const tar = require('tar');
const { fail } = require('assert');
const parser = require('@babel/parser');
const generator = require('@babel/generator').default;

const app = express();
const port = 3000;
const listen_addr = '0.0.0.0'


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

function parseFile(filePath) {
const code = fs.readFileSync(filePath, 'utf8');
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
});
return [ast,code];
}

function parseDirectory(directory) {
  const astTrees = [];
  let concatenatedCode = '';
  const files = fs.readdirSync(directory);

  files.forEach(file => {
      const filePath = path.join(directory, file);
      if (fs.lstatSync(filePath).isDirectory()) {
          const [subAstTrees, subConcatenatedCode] = parseDirectory(filePath);
          astTrees.push(...subAstTrees);
          concatenatedCode += subConcatenatedCode + '\n';
      } else if (filePath.endsWith('.js') || filePath.endsWith('.ts') || filePath.endsWith('.tsx')) {
          const [ast, code] = parseFile(filePath);
          removeLoc(ast);
          concatenatedCode += code + '\n';
          
          astTrees.push({
              file: filePath,
              ast,
          });
      }
  });
  return [astTrees, concatenatedCode];
}

function findShellScripts(directory, fileList = []) {
const files = fs.readdirSync(directory);

files.forEach(file => {
    const filePath = path.join(directory, file);
    if (fs.lstatSync(filePath).isDirectory()) {
    findShellScripts(filePath, fileList);
    } else if (filePath.endsWith('.sh')) {
    fileList.push(filePath);
    }
});

return fileList;
}
  
// Функция для чтения и объединения содержимого файлов
function concatenateShellScripts(fileList) {
let combinedContent = '';

fileList.forEach(file => {
    const fileContent = fs.readFileSync(file, 'utf8');
    const filteredContent = fileContent
    .split('\n')
    .filter(line => !line.startsWith('#!'))
    .join('\n');
    combinedContent += filteredContent + '\n';
});

return combinedContent;
}

function generateCodeFromAst(astTree) {
    if (Array.isArray(astTree)) {
      let combinedCode = '';
      astTree.forEach(item => {
        const generatedCode = generator(item.ast, {}).code;
        combinedCode += `// File: ${item.file}\n${generatedCode}\n`;
      });
      return combinedCode;
    } else {
      return generator(astTree, {}).code;
    }
  }



app.use(express.json());

app.post('/parse', async (req, res) => {
    const packageName = req.body.package;
    if (!packageName) {
        return res.status(400).json({ error: 'No package parameter provided' });
    }

    const tempDir = path.join(__dirname, 'temp');
    const packageDir = path.join(tempDir, packageName);
    

    if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir);
    }
    if (fs.existsSync(packageDir)) {
        fs.rmSync(packageDir, { recursive: true });
    }
    if (!fs.existsSync(packageDir)) {
        fs.mkdirSync(packageDir);
    }

    console.log(`Downloading package ${packageName}`);
    try {
        const tarFileName =  await new Promise((resolve, reject) => {
            exec(`npm pack ${packageName}`, { cwd: tempDir }, (error, stdout, stderr) => {
                if (error) {
                    return reject(error);
                }
                resolve(stdout.trim());
            });
        });

        await tar.extract({
            file: path.join(tempDir, tarFileName),
            cwd: packageDir
        });

        const rootDirectory = packageDir;
        const [astTreeArray,concatenatedCode] = parseDirectory(rootDirectory);
        const shellScripts = findShellScripts(rootDirectory);
        const concatenated = concatenateShellScripts(shellScripts);

        res.json({ast: astTreeArray, shell: concatenated, code: concatenatedCode});

    } catch (error) {
        console.log(error.message)
        res.status(500).json({ error: 'Failed to process package', details: error.message });
    } finally {
        if (fs.existsSync(packageDir)) {
            fs.rmSync(packageDir, { recursive: true });
        }
        if (fs.existsSync(tempDir)) {
            fs.rmSync(tempDir, { recursive: true });
        }
    }
});

app.post('/parsedir', async (req, res) => {
    const packagename = req.body.package;
    const directory = path.join('malware_samples/npm', packagename); // 'malware_samples/npm/express-4.17.1
    console.log(directory)
    if (!directory) {
        return res.status(400).json({ error: 'No directory parameter provided' });
    }
    if (!fs.existsSync(directory)) {
        return res.status(400).json({ error: 'Directory does not exist' });
    }
    try {
        const [astTreeArray,concatenatedCode] = parseDirectory(directory);
        const shellScripts = findShellScripts(directory);
        const concatenated = concatenateShellScripts(shellScripts);
        res.json({ast: astTreeArray, shell: concatenated, code: concatenatedCode});
    } catch (error) {
        res.status(500).json({ error: 'Failed to process directory', details: error.message });
    }
});

app.post('/asttocode', async (req, res) => {
    const ast = req.body.ast;
    if (!ast) {
        return res.status(400).json({ error: 'No ast parameter provided' });
    }
    try {
        const astTree = JSON.parse(ast);
        const generatedCode = generateCodeFromAst(astTree);
    
        res.json({code: generatedCode});
    } catch (error) {
        res.status(500).json({ error: 'Failed to generate code', details: error.message });
    } 
});


app.listen(port, listen_addr, () => {
    console.log(`Server is running on http://${listen_addr}:${port}`);
});