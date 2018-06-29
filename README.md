# BitTorrent Parser

## Key Concepts behind torrents

A Torrent file consists of integers, strings, lists, dictionaries

Each of the objects are encoded by a method called bencoding.

 * Strings - `<lengthOfString><separtor><stringVal> eg: 3:Sai`
 * Integers - `<'i'><numBase10><'e'>, ints are pre and post fixed by strings 'i' and 'e'. eg: i24e`
 * Lists - `<'l'><benCodedItems><'e'> eg: l3:SAIi24e4:spame is ['SAI', 24, 'spam']`
 * Dictionaries - `<'d'><alternatingKeyValue><'e'> eg: d3:sai4:bulk2:ksi24ee is {'sai': 'bulk', 'ks': 24}`
 * There may be torrents that have multiple files or single

 ## Usage
 * Check for Python installation, 2.7
 * To see it in action run `python torrparser <torrent_file_name>`
 * In the folder `test_files` are a few `.torrent` files that were quite hard to find. It was way easier 5 years back.

 ## Improvements
 * Writing tests is a good idea, would likely do that
 * Saw a few implementations using inner classes would like to try that
 * Having a command line help, like a man page is good idea too
 * Portability!

 ## Resources
 * [Wikipedia - Bencoding](https://en.wikipedia.org/wiki/Bencode)
 * [Torrent Files](https://en.wikipedia.org/wiki/Torrent_file)
 * [BitTorrent Protocol](http://www.bittorrent.org/beps/bep_0003.html)
 * [BencodePy](https://github.com/eweast/BencodePy)
 * [TorrentParser](https://github.com/7sDream/torrent_parser)
 * [TorrentParse](https://github.com/jamesbroadhead/torrentparse)
