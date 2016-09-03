def options(opt):
  opt.load('compiler_cxx')

def configure(conf):
  conf.env.CXXFLAGS += ['-O2', '-Wall', '-g', '-pipe']
  conf.load('compiler_cxx')
  conf.check_cfg(package='opencv', args='--cflags --libs')
  conf.check_cfg(package='jubatus-client', args='--cflags --libs')
  conf.check_cxx(lib = 'jubatus_core')

def build(bld):
  bld.shlib(
    source='image_feature.cpp',
    target='image_feature',
    use='OPENCV',
    install_path='${PREFIX}/lib/jubatus/plugin'
  )

  bld.program(
    source='test.cpp',
    target='test',
    use='JUBATUS_CORE image_feature')
