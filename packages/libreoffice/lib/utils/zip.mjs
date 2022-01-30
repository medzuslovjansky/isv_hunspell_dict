import 'zx/globals';
import archiver from 'archiver';

export async function zipFolder(src, dest) {
  const archive = archiver('zip', {
    zlib: { level: 9 } // Sets the compression level.
  });

  await fs.ensureDir(path.dirname(dest));
  const output = fs.createWriteStream(path.join(process.cwd(), dest));
  archive.pipe(output);

  return new Promise((resolve, reject) => {
    output.on('close', function() {
      console.log('Packed:', chalk.yellow(dest));
      resolve();
    });

    archive.on('warning', function(err) {
      if (err.code === 'ENOENT') {
        console.warn(err.message);
      } else {
        reject(err);
      }
    });

    archive.on('error', function(err) {
      reject(err);
    });

    archive.glob('**', {cwd: src });
    archive.finalize();
  });
}
