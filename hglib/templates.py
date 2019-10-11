from hglib.util import b

# changeset = b('{rev}\\0{node}\\0{tags}\\0{branch}\\0{author}'
#               '\\0{desc}\\0{date}\\0')
changeset = b('{rev}\\0{node}\\0{tags}\\0{branch}\\0{author}'
              '\\0{desc}\\0{date}\\0')

files = b('{rev}\\0')

