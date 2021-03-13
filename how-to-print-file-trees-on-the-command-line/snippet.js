const fs = require('fs')
const path = require('path')
const util = require('util')
const readdirPromise = util.promisify(fs.readdir)
const statPromise = util.promisify(fs.stat)

const buildTree = async (entity, indent, isHead, isTail, result) => {
    // determine if entity is a directory or file
    let stats = await statPromise(entity)
    let files = []
    if (stats.isDirectory()) {
        files = await readdirPromise(entity)
    }

    // keep track of line prefixes
    let entityPrefix = isTail === true ? '└── ' : '├── '
    let contentPrefix = isTail === true ? '    ' : '|   '
    if (isHead === true) {
        entityPrefix = ''
        contentPrefix = ''
    }

    // add entity to the output
    result += indent + entityPrefix + path.basename(entity) + '\n'

    // if entity is a directory, recurse through its contents
    for (let index = 0; index < files.length - 1; index++) {
        result = await buildTree(path.join(entity, files[index]), indent + contentPrefix, false, false, result)
    }
    if (files.length > 0) {
        result = await buildTree(path.join(entity, files[files.length - 1]), indent + contentPrefix, false, true, result)
    }
    return result
}

const generateFileTree = async (entity) => {
    let tree = await buildTree(entity, '', true, true, '')
    console.log(tree)
}
