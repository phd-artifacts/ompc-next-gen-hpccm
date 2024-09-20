"""
OMPC-NEXTGEN-DEV 0.0.1
This Image is used for development of OpenMP Cluster (OMPC) nextgen plugin on LLVM/OpenMP/Libomptarget.

Contents:
  Ubuntu 22.04
  CMAKE 3.29.0
  OmpCluster LLVM
  UCX 1.17.0
  MPICH 4.2.2
  TOOLS (git, ccache, wget, ninja-build, gdb)
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
# pylama: ignore=E0602

# add docstring to Dockerfile
Stage0 += comment(__doc__.strip(), reformat=False)

# Image recipe
Stage0 += comment('Set the ubuntu version to 22.04.')
Stage0 += baseimage(image='nvidia/cuda:12.0.0-devel-ubuntu20.04')

Stage0 += comment('Install the required packages.')

Stage0 += gnu()

# KNEM and XPMEM
Stage0 += knem(ldconfig=True)
Stage0 += xpmem(ldconfig=True)

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

# Tools
Stage0 += packages(
    apt=[
        'autoconf',
        'automake',
        'build-essential',
        'ca-certificates',
        'ccache',
        'gdb',
        'gfortran',
        'git',
        'gnupg',
        'gzip',
        'hwloc',
        'libelf-dev',
        'libfabric-dev',
        'libglib2.0-dev',
        'libgraphviz-dev',
        'libhwloc-dev',
        'libnuma-dev',
        'libssl-dev',
        'ninja-build',
        'openssh-client',
        'pdsh',
        'pkg-config',
        'wget',
    ],
)

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
Stage0 += comment('OpenBLAS/Lapack installation')
Stage0 += generic_cmake(cmake_opts=['-DCMAKE_BUILD_TYPE=Release',
                                    '-DBUILD_SHARED_LIBS=ON'],
                            url='https://github.com/xianyi/OpenBLAS/releases/download/v0.3.20/OpenBLAS-0.3.20.tar.gz')


# Compile LLVM
Stage0 += comment('Compile LLVM')
Stage0 += shell(commands= [
    'git clone --depth=1 -b offload-mpi-proxy-plugin https://github.com/cl3to/llvm-project /opt/llvm/llvm-project',
    'cmake -S/opt/llvm/llvm-project/llvm -B/opt/llvm/builds/llvm-project/release -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/llvm/installs/offload-mpi-plugin/release -DLLVM_ENABLE_PROJECTS=clang -DLLVM_ENABLE_RUNTIMES="offload;openmp;libcxx;libcxxabi;libunwind" -DLLVM_TARGETS_TO_BUILD="X86" -DCLANG_VENDOR=OmpCluster -DLIBOMPTARGET_ENABLE_DEBUG=1 -DLLVM_ENABLE_ASSERTIONS=On -DCMAKE_EXPORT_COMPILE_COMMANDS=On -DLLVM_INCLUDE_BENCHMARKS=Off -DLIBOMPTARGET_ENABLE_PROFILER=1 -DOPENMP_STANDALONE_BUILD=0 -DLIBOMPTARGET_PLUGINS_TO_BUILD="mpiproxy;host" -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -DLLVM_USE_LINKER=gold -DLLVM_CCACHE_BUILD=OFF -DLIBOMPTARGET_DEVICE_ARCHITECTURES=sm_70  -DOPENMP_ENABLE_LIBOMP_PROFILING=ON',
    'cmake --build /opt/llvm/builds/llvm-project/release -j',
    'cmake --install /opt/llvm/builds/llvm-project/release --prefix /opt/llvm/installs/offload-mpi-plugin/release',
    'rm -rf /opt/llvm/builds',
    'rm -rf /opt/llvm/llvm-project',
    'export PATH=/opt/llvm/installs/offload-mpi-plugin/release/bin:$PATH',
    'export LD_LIBRARY_PATH=/opt/llvm/installs/offload-mpi-plugin/release/lib/x86_64-unknown-linux-gnu:/opt/llvm/installs/offload-mpi-plugin/release/lib:$LD_LIBRARY_PATH',
    'export LIBRARY_PATH=/opt/llvm/installs/offload-mpi-plugin/release/lib:$LIBRARY_PATH',
    'export CPATH=$/opt/llvm/installs/offload-mpi-plugin/release/lib/clang/*/include:$CPATH',
    'export CC=clang',
    'export CXX=clang++'
])
Stage0 += environment(
    variables={
        'CC': 'clang',
        'CXX': 'clang++',
        'PATH': '/opt/llvm/installs/offload-mpi-plugin/release/bin:$PATH',
        'LD_LIBRARY_PATH': '/opt/llvm/installs/offload-mpi-plugin/release/lib/x86_64-unknown-linux-gnu:/opt/llvm/installs/offload-mpi-plugin/release/lib:$LD_LIBRARY_PATH',
        'LIBRARY_PATH': '/opt/llvm/installs/offload-mpi-plugin/release/lib:$LIBRARY_PATH',
        'CPATH':'$/opt/llvm/installs/offload-mpi-plugin/release/lib/clang/*/include:$CPATH'
    }
)
