const crypto = require('crypto')
const fs = require('fs')
const fetch = require('node-fetch')

// compute MD5 fingerprint from SSH public key
const fingerprint = async (pub) => {
    const pubre = /^(ssh-[dr]s[as]\s+)|(\s+.+)|\n/g
    const cleanpub = pub.replace(pubre, '')
    const pubbuffer = Buffer.from(cleanpub, 'base64')
    const key = hash(pubbuffer)
    return colons(key)
}

// compute MD5 hash
const hash = async (s) => {
    return crypto.createHash('md5').update(s).digest('hex')
}

// add colons, 'hello' => 'he:ll:o'
const colons = async (s) => {
    return s.replace(/(.{2})(?=.)/g, '$1:')
}

const createDroplet = async () => {
    // set up authentication
    let token = '<YOUR API TOKEN>'
    let sshKey = fs.readFileSync('~/.ssh/id_rsa.pub').toString()

    // configure droplet
    let configs = {
        name: 'my-test-droplet',
        region: 'sfo2',
        size: 's-1vcpu-1gb',
        image: 'ubuntu-18-04-x64',
        ssh_keys: [`${fingerprint(sshKey)}`],
        backups: false,
        ipv6: false,
        user_data: null,
        private_networking: null,
        volumes: null,
        tags: []
    }

    // create droplet with DigitalOcean API v2
    let response = await fetch('https://api.digitalocean.com/v2/droplets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(configs)
    })
    let data = await response.json()

    // report creation result
    if (data.droplet !== undefined) {
        console.log(`Created droplet: ${data.droplet.id}`)
    } else {
        console.error('Could not create droplet')
    }

    droplet = await waitForDroplet(data.droplet.id)
    console.log(`Status: ${droplet.status}`)
    console.log(`ID: ${droplet.id}`)
    console.log(`IP address: ${droplet.ip}`)
}

// wait for the droplet to become active
const waitForDroplet = async (id) => {
    let done = false
    let token = '<YOUR API TOKEN>'
    let droplet = null
    while (!done) {
        droplet = await inspectDroplet(id)
        if (droplet.status === 'active') {
            done = true
        }
    }
    return droplet
}

// inspect a droplet based on ID
const inspectDroplet = async (id) => {
    let result = {
        id: null,
        status: null,
        ip: null,
        error: null
    }
    let token = '<YOUR API TOKEN>'
    let response = await fetch(`https://api.digitalocean.com/v2/droplets/${id}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
    let data = await response.json()
    if (data.droplet === undefined) {
        result.error = data.message
        return result
    }
    result.id = data.droplet.id
    result.status = data.droplet.status
    if (result.status === 'active') {
        result.ip = data.droplet.networks.v4.filter(ip => ip.type === 'public')[0].ip_address
    }
    return result
}

createDroplet()

