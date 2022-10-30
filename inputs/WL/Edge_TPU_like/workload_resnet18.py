workload = {
    -1: {'equation': 'input',
         'loop_dim_size': {'B': 1, 'K': 3, 'OY': 224, 'OX': 224},
         'precision': 8,
         'core_allocation': 1,
         'memory_operand_links': {'O': 'I1'}
    }
    ,
    0: {  # conv1, stride 2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 3, 'OY': 311, 'OX': 311, 'FY': 7, 'FX': 7},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [-1]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'constant_operands': ['W'],
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 3), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    1: {  # max pool, stride 2
        'equation': 'O[b][g][oy][ox]+=W[fx][fy]*I[b][g][ix][iy]',
        'equation_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'G': 64, 'OY': 155, 'OX': 155, 'FX': 3, 'FY': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'I': 8, 'W': 0},
        'operand_source': {'W': [], 'I': [0]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    2: {  # conv2_1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 153, 'OX': 153, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [1]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    3: {  # conv2_2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 151, 'OX': 151, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [2]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    4: {  # Addition of layer 1 (residual path) and layer 3 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 64, 'OY': 151, 'OX': 151},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [1], 'Y': [3]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    5: {  # conv2_3
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 149, 'OX': 149, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [4]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    6: {  # conv2_4
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 64, 'C': 64, 'OY': 147, 'OX': 147, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [5]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    7: {  # Addition of layer 4 (residual connection) and layer 6 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 64, 'OY': 147, 'OX': 147},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [4], 'Y': [6]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    8: {  # conv3_1, stride 2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 64, 'OY': 73, 'OX': 73, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [7]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    9: {  # conv3_2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 128, 'OY': 71, 'OX': 71, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [8]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    10: {  # Addition of layer 7 (residual connection) and layer 9 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 128, 'OY': 71, 'OX': 71},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [7], 'Y': [9]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    11: {  # conv3_3
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 128, 'OY': 69, 'OX': 69, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [10]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    12: {  # conv3_4
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 128, 'C': 128, 'OY': 67, 'OX': 67, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [11]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    13: {  # Addition of layer 10 (residual connection) and layer 12 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 128, 'OY': 67, 'OX': 67},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [10], 'Y': [12]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    14: {  # conv4_1, stride 2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 128, 'OY': 33, 'OX': 33, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [13]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    15: {  # conv4_2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 256, 'OY': 31, 'OX': 31, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [14]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    16: {  # Addition of layer 13 (residual connection) and layer 15 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 256, 'OY': 31, 'OX': 31},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [13], 'Y': [15]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    17: {  # conv4_3
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 256, 'OY': 29, 'OX': 29, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [16]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    18: {  # conv4_4
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 256, 'C': 256, 'OY': 27, 'OX': 27, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [17]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    19: {  # Addition of layer 16 (residual connection) and layer 18 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 256, 'OY': 27, 'OX': 27},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [16], 'Y': [18]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    20: {  # conv5_1, stride 2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 256, 'OY': 13, 'OX': 13, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [19]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    21: {  # conv5_2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 11, 'OX': 11, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [20]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    22: {  # Addition of layer 19 (residual connection) and layer 21 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 512, 'OY': 11, 'OX': 11},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [19], 'Y': [21]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    23: {  # conv5_3
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 9, 'OX': 9, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [22]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    24: {  # conv5_4
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 7, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [23]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
    ,
    25: {  # Addition of layer 22 (residual connection) and layer 24 (main path)
        'equation': 'O[b][g][oy][ox]=X[b][g][oy][ox]+Y[b][g][oy][ox]',
        'equation_relations': [],
        'loop_dim_size': {'B': 1, 'G': 512, 'OY': 7, 'OX': 7},
        'operand_precision': {'O': 16, 'O_final': 8, 'X': 8, 'Y': 8},
        'operand_source': {'X': [22], 'Y': [24]},
        'constant_operands': [],
        'operand_source_dimension_mapping': {'X': {'OX': 'OX', 'OY': 'OY', 'G': 'G'}, 'Y': {'OX': 'OX', 'OY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8), 'D3': ('OX', 4), 'D4': ('OY', 4)},
        'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    }
    ,
    26: {  # aver pool
        'equation': 'O[b][g][oy][ox]+=W[fx][fy]*I[b][g][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'G': 512, 'OY': 1, 'OX': 1, 'FX': 7, 'FY': 7},
        'operand_precision': {'O': 16, 'O_final': 8, 'I': 8, 'W': 0},
        'operand_source': {'W': [], 'I': [25]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'G': 'K'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('G', 8)},
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    },
    27: {  # fc
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'equation_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 1000, 'C': 512, 'OY': 1, 'OX': 1, 'FY': 1, 'FX': 1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [26]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'core_allocation': 1,
        'spatial_mapping': {'D1': ('K', 8), 'D2': ('C', 8)},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
    }
}
