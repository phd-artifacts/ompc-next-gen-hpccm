"""
OMPC-NEXTGEN-DEV 0.0.1
This Image is used for development of OpenMP Cluster (OMPC) nextgen plugin on LLVM/OpenMP/Libomptarget.

Contents:
  Ubuntu 22.04
  CMAKE 3.29.0
  OmpCluster LLVM
  UCX 1.17.0
  MPICH 4.2.2
  TOOLS (git, ccache, wget, ninja-build, gdb, zsh)
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
# pylama: ignore=E0602

# add docstring to Dockerfile
Stage0 += comment(__doc__.strip(), reformat=False)

# Image recipe
Stage0 += comment('Set the ubuntu version to 22.04.')
Stage0 += baseimage(image='nvidia/cuda:12.0.0-devel-ubuntu22.04')

Stage0 += comment('Install the required packages.')

Stage0 += gnu()

# KNEM and XPMEM
Stage0 += knem(ldconfig=True)
Stage0 += xpmem(ldconfig=True)

# Tools
Stage0 += packages(
    apt=[
        'autoconf',
        'automake',
        'build-essential',
        'ca-certificates',
        'ccache',
        'gdb',
        'gdbserver',
        'gfortran',
        'git',
        'gnupg',
        'gzip',
        'hwloc',
        'libelf-dev',
        'libfabric-dev',
        'libglib2.0-dev',
        'liburing-dev',
        'libgraphviz-dev',
        'libhwloc-dev',
        'libnuma-dev',
        'librdmacm-dev',
        'liburing-dev',
        'libssl-dev',
        'ninja-build',
        'openssh-client',
        'pdsh',
        'pkg-config',
        'wget',
        'zsh',  # Added zsh to the list of tools
    ],
)

# UCX
ucx = ucx(
    version='1.17.0',
    cuda=True,
    knem="/usr/local/knem",
    ldconfig=True,
    ofed=True,
    xpmem="/usr/local/xpmem",
)
Stage0 += ucx

# Python
python = python(python2=False, devel=True)
Stage0 += python

Stage0 += packages(
    apt=[
        'python3-distutils',
        'python3-psutil',
    ]
)

# Pip
Stage0 += pip(pip='pip3', packages=['numpy', 'matplotlib', 'findiff', 'gdown', 'h5py'])

# CMAKE
Stage0 += cmake(eula=True, version='3.29.0')

# LLVM
llvm = llvm(
    upstream=True,
    version='17',
    openmp=True,
    toolset=True,
)
Stage0 += llvm
Stage0 += llvm.runtime()

Stage0 += environment(
    variables={
        'CC': '/usr/bin/clang',
        'CXX': '/usr/bin/clang++',
        'LIBRARY_PATH': '/usr/lib/x86_64-linux-gnu/:/usr/local/lib:$LIBRARY_PATH',
        'LD_LIBRARY_PATH': '/usr/lib/x86_64-linux-gnu/:/usr/local/lib:$LD_LIBRARY_PATH',
    }
)

# MPICH
mpich = mpich(
    version='4.2.2',
    with_ucx='/usr/local/ucx',
    with_device='ch4:ucx',
)
Stage0 += mpich

Stage0 += comment('Set the environment variables.')
Stage0 += environment(
    variables={
        'CPATH': '/usr/local/mpich/include:$CPATH',
    }
)

# Nsight
Stage0 += nsight_systems(version='2024.2.1', cli=False)
Stage0 += nsight_compute(version='2024.2.1')

Stage0 += gnu(version=10)

# Install OpenBlas/Lapack
#Stage0 += comment('OpenBLAS/Lapack installation')
#Stage0 += generic_cmake(
#    cmake_opts=[
#        '-DCMAKE_BUILD_TYPE=Release',
#        '-DBUILD_SHARED_LIBS=ON'
#    ],
#    url='https://github.com/xianyi/OpenBLAS/releases/download/v0.3.20/OpenBLAS-0.3.20.tar.gz'
#)

