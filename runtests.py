#!/usr/bin/env python


def runtests():
    import nose
    argv = []
    argv.insert(1, '')
    argv.insert(2, '--with-coverage')
    argv.insert(3, '--cover-package=facio')
    nose.main(argv=argv)


if __name__ == '__main__':
    runtests()
