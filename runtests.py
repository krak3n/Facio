#!/usr/bin/env python


def runtests():
    import nose
    argv = []
    argv.insert(1, '')
    argv.insert(2, '--with-spec')
    argv.insert(3, '--spec-color')
    argv.insert(4, '--with-coverage')
    argv.insert(5, '--cover-erase')
    argv.insert(6, '--cover-package=facio')
    nose.main(argv=argv)


if __name__ == '__main__':
    runtests()
