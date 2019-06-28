const readline = require('readline');
const fs = require('fs')
const spawn = require("child_process").spawn;
let {PythonShell} = require('python-shell')

let rawdata = fs.readFileSync('./package.json');
let data = JSON.parse(rawdata);
const path = data.tokens

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans);
    }))
}

if (fs.existsSync(path)) {
    PythonShell.run('./src/main.py', function (err) {
      if (err) throw err;
    });
} else {
  console.log("Miscord was not able to detect a tokens.json file in the current directory.")
  rl.question('Have it on another directory? Specify it here (leave in blank if not): ', (answer) => {
      if (fs.existsSync(answer)) {
        var newData = JSON.stringify(data).replace(/tokens/g, `"${answer}"`); //convert to JSON string
        fs.truncate('package.json', 0, function(){
          fs.writeFile('package.json', newData, 'utf8', callback);
        });
        newDataParsed = JSON.parse(newData)
        fs.appendFile('.gitignore', newData.tokens, function (err) {
          if (err) throw err;
        });
        PythonShell.run('./src/main.py', function (err) {
          if (err) throw err;
        });
      } else {
        console.log("\nMiscord was not able to detect a tokens.json file in the specified directory. It will now proceed to generate it.")
        const ans = askQuestion("\nDiscord bot app token (https://discordapp.com/developers): ");
        console.log(`\tBot token: ${ans}`);

        var tokensJSON = {
           table: []
        };

        const ans2 = askQuestion("\t\tGenius lib token: ");
        console.log(`\t\t\tGenius token: ${ans2}`);
        tokensJSON.table.push({discord_bot_token: ans, genius_login_token: ans2});
        var json = JSON.stringify(tokensJSON);
        fs.writeFile('tokens.json', json, 'utf8', callback);
        console.log("Generated file")
        fs.appendFile('.gitignore', path, function (err) {
          if (err) throw err;
        });
        PythonShell.run('./src/main.py', function (err) {
          if (err) throw err;
        });
      }
    });
}
