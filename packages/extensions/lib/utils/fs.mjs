import 'zx/globals';

import tar from 'tar';

export async function recreateDirectory(dirName) {
  await fs.remove(path.resolve(dirName));
  console.log('Removed directory: ' + chalk.yellow(dirName));
  await fs.mkdirp(path.resolve(dirName));
  console.log('Created directory: ' + chalk.yellow(dirName));
}

export async function copyFile(src, dest) {
  await fs.ensureDir(path.dirname(path.resolve(dest)));
  await fs.copyFile(path.resolve(src), path.resolve(dest));
  console.log('Copied:', chalk.yellow(dest));
}
