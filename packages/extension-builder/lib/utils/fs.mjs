import 'zx/globals';

export async function recreateDirectory(dirName) {
  await fs.remove(path.resolve(dirName));
  await fs.mkdirp(path.resolve(dirName));
}

export async function copyFile({ sourceFile, outFile }) {
  await fs.ensureDir(path.dirname(path.resolve(outFile)));
  await fs.copyFile(path.resolve(sourceFile), path.resolve(outFile));
}
