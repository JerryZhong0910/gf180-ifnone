// Copyright 2022 GlobalFoundries PDK Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

module gf180mcu_fd_sc_mcu9t5v0__mux4_2( I2, S0, I3, Z, S1, I1, I0 );
input I0, I1, I2, I3, S0, S1;
output Z;

   `ifdef FUNCTIONAL  //  functional //

	gf180mcu_fd_sc_mcu9t5v0__mux4_2_func gf180mcu_fd_sc_mcu9t5v0__mux4_2_behav_inst(.I2(I2),.S0(S0),.I3(I3),.Z(Z),.S1(S1),.I1(I1),.I0(I0));

   `else

	gf180mcu_fd_sc_mcu9t5v0__mux4_2_func gf180mcu_fd_sc_mcu9t5v0__mux4_2_inst(.I2(I2),.S0(S0),.I3(I3),.Z(Z),.S1(S1),.I1(I1),.I0(I0));

	// spec_gates_begin


	// spec_gates_end


wand __gls_path_I0_Z_8424b6dbc4680811; assign __gls_path_I0_Z_8424b6dbc4680811 = (I1 === 1'b0); assign __gls_path_I0_Z_8424b6dbc4680811 = (I2 === 1'b0); assign __gls_path_I0_Z_8424b6dbc4680811 = (I3 === 1'b0); wand __gls_path_I0_Z_83191c966c6bd00e; assign __gls_path_I0_Z_83191c966c6bd00e = (I1 === 1'b0); assign __gls_path_I0_Z_83191c966c6bd00e = (I2 === 1'b0); assign __gls_path_I0_Z_83191c966c6bd00e = (I3 === 1'b1); wand __gls_path_I0_Z_b39edf9ea62c935a; assign __gls_path_I0_Z_b39edf9ea62c935a = (I1 === 1'b0); assign __gls_path_I0_Z_b39edf9ea62c935a = (I2 === 1'b1); assign __gls_path_I0_Z_b39edf9ea62c935a = (I3 === 1'b0); wand __gls_path_I0_Z_9f9cfb3ff7f8f549; assign __gls_path_I0_Z_9f9cfb3ff7f8f549 = (I1 === 1'b0); assign __gls_path_I0_Z_9f9cfb3ff7f8f549 = (I2 === 1'b1); assign __gls_path_I0_Z_9f9cfb3ff7f8f549 = (I3 === 1'b1); wand __gls_path_I0_Z_4d79bffca87523db; assign __gls_path_I0_Z_4d79bffca87523db = (I1 === 1'b1); assign __gls_path_I0_Z_4d79bffca87523db = (I2 === 1'b0); assign __gls_path_I0_Z_4d79bffca87523db = (I3 === 1'b0); wand __gls_path_I0_Z_7bd67582ae5bebe5; assign __gls_path_I0_Z_7bd67582ae5bebe5 = (I1 === 1'b1); assign __gls_path_I0_Z_7bd67582ae5bebe5 = (I2 === 1'b0); assign __gls_path_I0_Z_7bd67582ae5bebe5 = (I3 === 1'b1); wand __gls_path_I0_Z_41238af02176fcc7; assign __gls_path_I0_Z_41238af02176fcc7 = (I1 === 1'b1); assign __gls_path_I0_Z_41238af02176fcc7 = (I2 === 1'b1); assign __gls_path_I0_Z_41238af02176fcc7 = (I3 === 1'b0); wand __gls_path_I0_Z_1123258cc126892e; assign __gls_path_I0_Z_1123258cc126892e = (I1 === 1'b1); assign __gls_path_I0_Z_1123258cc126892e = (I2 === 1'b1); assign __gls_path_I0_Z_1123258cc126892e = (I3 === 1'b1); wor __gls_path_I0_Z_any; assign __gls_path_I0_Z_any = __gls_path_I0_Z_8424b6dbc4680811; assign __gls_path_I0_Z_any = __gls_path_I0_Z_83191c966c6bd00e; assign __gls_path_I0_Z_any = __gls_path_I0_Z_b39edf9ea62c935a; assign __gls_path_I0_Z_any = __gls_path_I0_Z_9f9cfb3ff7f8f549; assign __gls_path_I0_Z_any = __gls_path_I0_Z_4d79bffca87523db; assign __gls_path_I0_Z_any = __gls_path_I0_Z_7bd67582ae5bebe5; assign __gls_path_I0_Z_any = __gls_path_I0_Z_41238af02176fcc7; assign __gls_path_I0_Z_any = __gls_path_I0_Z_1123258cc126892e; wire __gls_path_I0_Z_fallback; assign __gls_path_I0_Z_fallback = (__gls_path_I0_Z_any === 1'b0); wand __gls_path_I1_Z_e833a296af4d937f; assign __gls_path_I1_Z_e833a296af4d937f = (I0 === 1'b0); assign __gls_path_I1_Z_e833a296af4d937f = (I2 === 1'b0); assign __gls_path_I1_Z_e833a296af4d937f = (I3 === 1'b0); wand __gls_path_I1_Z_dd6ae494df461d4b; assign __gls_path_I1_Z_dd6ae494df461d4b = (I0 === 1'b0); assign __gls_path_I1_Z_dd6ae494df461d4b = (I2 === 1'b0); assign __gls_path_I1_Z_dd6ae494df461d4b = (I3 === 1'b1); wand __gls_path_I1_Z_7cbec624fd6405ec; assign __gls_path_I1_Z_7cbec624fd6405ec = (I0 === 1'b0); assign __gls_path_I1_Z_7cbec624fd6405ec = (I2 === 1'b1); assign __gls_path_I1_Z_7cbec624fd6405ec = (I3 === 1'b0); wand __gls_path_I1_Z_c4da6787f333b0d9; assign __gls_path_I1_Z_c4da6787f333b0d9 = (I0 === 1'b0); assign __gls_path_I1_Z_c4da6787f333b0d9 = (I2 === 1'b1); assign __gls_path_I1_Z_c4da6787f333b0d9 = (I3 === 1'b1); wand __gls_path_I1_Z_98bc95088385fdcd; assign __gls_path_I1_Z_98bc95088385fdcd = (I0 === 1'b1); assign __gls_path_I1_Z_98bc95088385fdcd = (I2 === 1'b0); assign __gls_path_I1_Z_98bc95088385fdcd = (I3 === 1'b0); wand __gls_path_I1_Z_4383d1922b09e632; assign __gls_path_I1_Z_4383d1922b09e632 = (I0 === 1'b1); assign __gls_path_I1_Z_4383d1922b09e632 = (I2 === 1'b0); assign __gls_path_I1_Z_4383d1922b09e632 = (I3 === 1'b1); wand __gls_path_I1_Z_d1d9599cb6edef01; assign __gls_path_I1_Z_d1d9599cb6edef01 = (I0 === 1'b1); assign __gls_path_I1_Z_d1d9599cb6edef01 = (I2 === 1'b1); assign __gls_path_I1_Z_d1d9599cb6edef01 = (I3 === 1'b0); wand __gls_path_I1_Z_166fc1a64d1b4a5d; assign __gls_path_I1_Z_166fc1a64d1b4a5d = (I0 === 1'b1); assign __gls_path_I1_Z_166fc1a64d1b4a5d = (I2 === 1'b1); assign __gls_path_I1_Z_166fc1a64d1b4a5d = (I3 === 1'b1); wor __gls_path_I1_Z_any; assign __gls_path_I1_Z_any = __gls_path_I1_Z_e833a296af4d937f; assign __gls_path_I1_Z_any = __gls_path_I1_Z_dd6ae494df461d4b; assign __gls_path_I1_Z_any = __gls_path_I1_Z_7cbec624fd6405ec; assign __gls_path_I1_Z_any = __gls_path_I1_Z_c4da6787f333b0d9; assign __gls_path_I1_Z_any = __gls_path_I1_Z_98bc95088385fdcd; assign __gls_path_I1_Z_any = __gls_path_I1_Z_4383d1922b09e632; assign __gls_path_I1_Z_any = __gls_path_I1_Z_d1d9599cb6edef01; assign __gls_path_I1_Z_any = __gls_path_I1_Z_166fc1a64d1b4a5d; wire __gls_path_I1_Z_fallback; assign __gls_path_I1_Z_fallback = (__gls_path_I1_Z_any === 1'b0); wand __gls_path_I2_Z_8b9df3811a837233; assign __gls_path_I2_Z_8b9df3811a837233 = (I0 === 1'b0); assign __gls_path_I2_Z_8b9df3811a837233 = (I1 === 1'b0); assign __gls_path_I2_Z_8b9df3811a837233 = (I3 === 1'b0); wand __gls_path_I2_Z_6e14929d86731def; assign __gls_path_I2_Z_6e14929d86731def = (I0 === 1'b0); assign __gls_path_I2_Z_6e14929d86731def = (I1 === 1'b0); assign __gls_path_I2_Z_6e14929d86731def = (I3 === 1'b1); wand __gls_path_I2_Z_20e72c62277d77eb; assign __gls_path_I2_Z_20e72c62277d77eb = (I0 === 1'b0); assign __gls_path_I2_Z_20e72c62277d77eb = (I1 === 1'b1); assign __gls_path_I2_Z_20e72c62277d77eb = (I3 === 1'b0); wand __gls_path_I2_Z_13b58e70d7e1ef98; assign __gls_path_I2_Z_13b58e70d7e1ef98 = (I0 === 1'b0); assign __gls_path_I2_Z_13b58e70d7e1ef98 = (I1 === 1'b1); assign __gls_path_I2_Z_13b58e70d7e1ef98 = (I3 === 1'b1); wand __gls_path_I2_Z_1c4766127897e6db; assign __gls_path_I2_Z_1c4766127897e6db = (I0 === 1'b1); assign __gls_path_I2_Z_1c4766127897e6db = (I1 === 1'b0); assign __gls_path_I2_Z_1c4766127897e6db = (I3 === 1'b0); wand __gls_path_I2_Z_01b7b437d913054d; assign __gls_path_I2_Z_01b7b437d913054d = (I0 === 1'b1); assign __gls_path_I2_Z_01b7b437d913054d = (I1 === 1'b0); assign __gls_path_I2_Z_01b7b437d913054d = (I3 === 1'b1); wand __gls_path_I2_Z_8f3bdd1eb1a0c93f; assign __gls_path_I2_Z_8f3bdd1eb1a0c93f = (I0 === 1'b1); assign __gls_path_I2_Z_8f3bdd1eb1a0c93f = (I1 === 1'b1); assign __gls_path_I2_Z_8f3bdd1eb1a0c93f = (I3 === 1'b0); wand __gls_path_I2_Z_554dcf7858300e77; assign __gls_path_I2_Z_554dcf7858300e77 = (I0 === 1'b1); assign __gls_path_I2_Z_554dcf7858300e77 = (I1 === 1'b1); assign __gls_path_I2_Z_554dcf7858300e77 = (I3 === 1'b1); wor __gls_path_I2_Z_any; assign __gls_path_I2_Z_any = __gls_path_I2_Z_8b9df3811a837233; assign __gls_path_I2_Z_any = __gls_path_I2_Z_6e14929d86731def; assign __gls_path_I2_Z_any = __gls_path_I2_Z_20e72c62277d77eb; assign __gls_path_I2_Z_any = __gls_path_I2_Z_13b58e70d7e1ef98; assign __gls_path_I2_Z_any = __gls_path_I2_Z_1c4766127897e6db; assign __gls_path_I2_Z_any = __gls_path_I2_Z_01b7b437d913054d; assign __gls_path_I2_Z_any = __gls_path_I2_Z_8f3bdd1eb1a0c93f; assign __gls_path_I2_Z_any = __gls_path_I2_Z_554dcf7858300e77; wire __gls_path_I2_Z_fallback; assign __gls_path_I2_Z_fallback = (__gls_path_I2_Z_any === 1'b0); wand __gls_path_I3_Z_0a58f28ebd63d02b; assign __gls_path_I3_Z_0a58f28ebd63d02b = (I0 === 1'b0); assign __gls_path_I3_Z_0a58f28ebd63d02b = (I1 === 1'b0); assign __gls_path_I3_Z_0a58f28ebd63d02b = (I2 === 1'b0); wand __gls_path_I3_Z_0daf45bc27540240; assign __gls_path_I3_Z_0daf45bc27540240 = (I0 === 1'b0); assign __gls_path_I3_Z_0daf45bc27540240 = (I1 === 1'b0); assign __gls_path_I3_Z_0daf45bc27540240 = (I2 === 1'b1); wand __gls_path_I3_Z_76d4c04a0abdc208; assign __gls_path_I3_Z_76d4c04a0abdc208 = (I0 === 1'b0); assign __gls_path_I3_Z_76d4c04a0abdc208 = (I1 === 1'b1); assign __gls_path_I3_Z_76d4c04a0abdc208 = (I2 === 1'b0); wand __gls_path_I3_Z_6acbb16535a1e437; assign __gls_path_I3_Z_6acbb16535a1e437 = (I0 === 1'b0); assign __gls_path_I3_Z_6acbb16535a1e437 = (I1 === 1'b1); assign __gls_path_I3_Z_6acbb16535a1e437 = (I2 === 1'b1); wand __gls_path_I3_Z_9f812ef8ee180d3d; assign __gls_path_I3_Z_9f812ef8ee180d3d = (I0 === 1'b1); assign __gls_path_I3_Z_9f812ef8ee180d3d = (I1 === 1'b0); assign __gls_path_I3_Z_9f812ef8ee180d3d = (I2 === 1'b0); wand __gls_path_I3_Z_e4c2c1ade9b4492a; assign __gls_path_I3_Z_e4c2c1ade9b4492a = (I0 === 1'b1); assign __gls_path_I3_Z_e4c2c1ade9b4492a = (I1 === 1'b0); assign __gls_path_I3_Z_e4c2c1ade9b4492a = (I2 === 1'b1); wand __gls_path_I3_Z_68582c3e98962e4c; assign __gls_path_I3_Z_68582c3e98962e4c = (I0 === 1'b1); assign __gls_path_I3_Z_68582c3e98962e4c = (I1 === 1'b1); assign __gls_path_I3_Z_68582c3e98962e4c = (I2 === 1'b0); wand __gls_path_I3_Z_378b8deebd8c3b7d; assign __gls_path_I3_Z_378b8deebd8c3b7d = (I0 === 1'b1); assign __gls_path_I3_Z_378b8deebd8c3b7d = (I1 === 1'b1); assign __gls_path_I3_Z_378b8deebd8c3b7d = (I2 === 1'b1); wor __gls_path_I3_Z_any; assign __gls_path_I3_Z_any = __gls_path_I3_Z_0a58f28ebd63d02b; assign __gls_path_I3_Z_any = __gls_path_I3_Z_0daf45bc27540240; assign __gls_path_I3_Z_any = __gls_path_I3_Z_76d4c04a0abdc208; assign __gls_path_I3_Z_any = __gls_path_I3_Z_6acbb16535a1e437; assign __gls_path_I3_Z_any = __gls_path_I3_Z_9f812ef8ee180d3d; assign __gls_path_I3_Z_any = __gls_path_I3_Z_e4c2c1ade9b4492a; assign __gls_path_I3_Z_any = __gls_path_I3_Z_68582c3e98962e4c; assign __gls_path_I3_Z_any = __gls_path_I3_Z_378b8deebd8c3b7d; wire __gls_path_I3_Z_fallback; assign __gls_path_I3_Z_fallback = (__gls_path_I3_Z_any === 1'b0); wand __gls_path_S0_Z_5d98abc676625da0; assign __gls_path_S0_Z_5d98abc676625da0 = (I0 === 1'b0); assign __gls_path_S0_Z_5d98abc676625da0 = (I1 === 1'b0); assign __gls_path_S0_Z_5d98abc676625da0 = (I2 === 1'b1); assign __gls_path_S0_Z_5d98abc676625da0 = (I3 === 1'b0); assign __gls_path_S0_Z_5d98abc676625da0 = (S1 === 1'b1); wand __gls_path_S0_Z_ff4583194436cdf2; assign __gls_path_S0_Z_ff4583194436cdf2 = (I0 === 1'b0); assign __gls_path_S0_Z_ff4583194436cdf2 = (I1 === 1'b1); assign __gls_path_S0_Z_ff4583194436cdf2 = (I2 === 1'b1); assign __gls_path_S0_Z_ff4583194436cdf2 = (I3 === 1'b0); assign __gls_path_S0_Z_ff4583194436cdf2 = (S1 === 1'b1); wand __gls_path_S0_Z_7af0c6f2bcc175a8; assign __gls_path_S0_Z_7af0c6f2bcc175a8 = (I0 === 1'b1); assign __gls_path_S0_Z_7af0c6f2bcc175a8 = (I1 === 1'b0); assign __gls_path_S0_Z_7af0c6f2bcc175a8 = (I2 === 1'b0); assign __gls_path_S0_Z_7af0c6f2bcc175a8 = (I3 === 1'b0); assign __gls_path_S0_Z_7af0c6f2bcc175a8 = (S1 === 1'b0); wand __gls_path_S0_Z_24cecb18cd43c5c0; assign __gls_path_S0_Z_24cecb18cd43c5c0 = (I0 === 1'b1); assign __gls_path_S0_Z_24cecb18cd43c5c0 = (I1 === 1'b0); assign __gls_path_S0_Z_24cecb18cd43c5c0 = (I2 === 1'b0); assign __gls_path_S0_Z_24cecb18cd43c5c0 = (I3 === 1'b1); assign __gls_path_S0_Z_24cecb18cd43c5c0 = (S1 === 1'b0); wand __gls_path_S0_Z_6a3c1955b4a12a06; assign __gls_path_S0_Z_6a3c1955b4a12a06 = (I0 === 1'b1); assign __gls_path_S0_Z_6a3c1955b4a12a06 = (I1 === 1'b0); assign __gls_path_S0_Z_6a3c1955b4a12a06 = (I2 === 1'b1); assign __gls_path_S0_Z_6a3c1955b4a12a06 = (I3 === 1'b0); assign __gls_path_S0_Z_6a3c1955b4a12a06 = (S1 === 1'b0); wand __gls_path_S0_Z_0366c29772b1d9e0; assign __gls_path_S0_Z_0366c29772b1d9e0 = (I0 === 1'b1); assign __gls_path_S0_Z_0366c29772b1d9e0 = (I1 === 1'b0); assign __gls_path_S0_Z_0366c29772b1d9e0 = (I2 === 1'b1); assign __gls_path_S0_Z_0366c29772b1d9e0 = (I3 === 1'b0); assign __gls_path_S0_Z_0366c29772b1d9e0 = (S1 === 1'b1); wand __gls_path_S0_Z_984ead1fbe50c218; assign __gls_path_S0_Z_984ead1fbe50c218 = (I0 === 1'b1); assign __gls_path_S0_Z_984ead1fbe50c218 = (I1 === 1'b0); assign __gls_path_S0_Z_984ead1fbe50c218 = (I2 === 1'b1); assign __gls_path_S0_Z_984ead1fbe50c218 = (I3 === 1'b1); assign __gls_path_S0_Z_984ead1fbe50c218 = (S1 === 1'b0); wand __gls_path_S0_Z_4e2b01c2992e2c7a; assign __gls_path_S0_Z_4e2b01c2992e2c7a = (I0 === 1'b1); assign __gls_path_S0_Z_4e2b01c2992e2c7a = (I1 === 1'b1); assign __gls_path_S0_Z_4e2b01c2992e2c7a = (I2 === 1'b1); assign __gls_path_S0_Z_4e2b01c2992e2c7a = (I3 === 1'b0); assign __gls_path_S0_Z_4e2b01c2992e2c7a = (S1 === 1'b1); wand __gls_path_S0_Z_4bf5f7f930cd881b; assign __gls_path_S0_Z_4bf5f7f930cd881b = (I0 === 1'b0); assign __gls_path_S0_Z_4bf5f7f930cd881b = (I1 === 1'b0); assign __gls_path_S0_Z_4bf5f7f930cd881b = (I2 === 1'b0); assign __gls_path_S0_Z_4bf5f7f930cd881b = (I3 === 1'b1); assign __gls_path_S0_Z_4bf5f7f930cd881b = (S1 === 1'b1); wand __gls_path_S0_Z_fbae8866159e5dd6; assign __gls_path_S0_Z_fbae8866159e5dd6 = (I0 === 1'b0); assign __gls_path_S0_Z_fbae8866159e5dd6 = (I1 === 1'b1); assign __gls_path_S0_Z_fbae8866159e5dd6 = (I2 === 1'b0); assign __gls_path_S0_Z_fbae8866159e5dd6 = (I3 === 1'b0); assign __gls_path_S0_Z_fbae8866159e5dd6 = (S1 === 1'b0); wand __gls_path_S0_Z_fbbdc4496fadfc31; assign __gls_path_S0_Z_fbbdc4496fadfc31 = (I0 === 1'b0); assign __gls_path_S0_Z_fbbdc4496fadfc31 = (I1 === 1'b1); assign __gls_path_S0_Z_fbbdc4496fadfc31 = (I2 === 1'b0); assign __gls_path_S0_Z_fbbdc4496fadfc31 = (I3 === 1'b1); assign __gls_path_S0_Z_fbbdc4496fadfc31 = (S1 === 1'b0); wand __gls_path_S0_Z_42ae265a4bafd07f; assign __gls_path_S0_Z_42ae265a4bafd07f = (I0 === 1'b0); assign __gls_path_S0_Z_42ae265a4bafd07f = (I1 === 1'b1); assign __gls_path_S0_Z_42ae265a4bafd07f = (I2 === 1'b0); assign __gls_path_S0_Z_42ae265a4bafd07f = (I3 === 1'b1); assign __gls_path_S0_Z_42ae265a4bafd07f = (S1 === 1'b1); wand __gls_path_S0_Z_9c78918d92ffb60d; assign __gls_path_S0_Z_9c78918d92ffb60d = (I0 === 1'b0); assign __gls_path_S0_Z_9c78918d92ffb60d = (I1 === 1'b1); assign __gls_path_S0_Z_9c78918d92ffb60d = (I2 === 1'b1); assign __gls_path_S0_Z_9c78918d92ffb60d = (I3 === 1'b0); assign __gls_path_S0_Z_9c78918d92ffb60d = (S1 === 1'b0); wand __gls_path_S0_Z_66a47733f2164099; assign __gls_path_S0_Z_66a47733f2164099 = (I0 === 1'b0); assign __gls_path_S0_Z_66a47733f2164099 = (I1 === 1'b1); assign __gls_path_S0_Z_66a47733f2164099 = (I2 === 1'b1); assign __gls_path_S0_Z_66a47733f2164099 = (I3 === 1'b1); assign __gls_path_S0_Z_66a47733f2164099 = (S1 === 1'b0); wand __gls_path_S0_Z_edd38b5397ef7ab0; assign __gls_path_S0_Z_edd38b5397ef7ab0 = (I0 === 1'b1); assign __gls_path_S0_Z_edd38b5397ef7ab0 = (I1 === 1'b0); assign __gls_path_S0_Z_edd38b5397ef7ab0 = (I2 === 1'b0); assign __gls_path_S0_Z_edd38b5397ef7ab0 = (I3 === 1'b1); assign __gls_path_S0_Z_edd38b5397ef7ab0 = (S1 === 1'b1); wand __gls_path_S0_Z_55b7162a8a034075; assign __gls_path_S0_Z_55b7162a8a034075 = (I0 === 1'b1); assign __gls_path_S0_Z_55b7162a8a034075 = (I1 === 1'b1); assign __gls_path_S0_Z_55b7162a8a034075 = (I2 === 1'b0); assign __gls_path_S0_Z_55b7162a8a034075 = (I3 === 1'b1); assign __gls_path_S0_Z_55b7162a8a034075 = (S1 === 1'b1); wor __gls_path_S0_Z_any; assign __gls_path_S0_Z_any = __gls_path_S0_Z_5d98abc676625da0; assign __gls_path_S0_Z_any = __gls_path_S0_Z_ff4583194436cdf2; assign __gls_path_S0_Z_any = __gls_path_S0_Z_7af0c6f2bcc175a8; assign __gls_path_S0_Z_any = __gls_path_S0_Z_24cecb18cd43c5c0; assign __gls_path_S0_Z_any = __gls_path_S0_Z_6a3c1955b4a12a06; assign __gls_path_S0_Z_any = __gls_path_S0_Z_0366c29772b1d9e0; assign __gls_path_S0_Z_any = __gls_path_S0_Z_984ead1fbe50c218; assign __gls_path_S0_Z_any = __gls_path_S0_Z_4e2b01c2992e2c7a; assign __gls_path_S0_Z_any = __gls_path_S0_Z_4bf5f7f930cd881b; assign __gls_path_S0_Z_any = __gls_path_S0_Z_fbae8866159e5dd6; assign __gls_path_S0_Z_any = __gls_path_S0_Z_fbbdc4496fadfc31; assign __gls_path_S0_Z_any = __gls_path_S0_Z_42ae265a4bafd07f; assign __gls_path_S0_Z_any = __gls_path_S0_Z_9c78918d92ffb60d; assign __gls_path_S0_Z_any = __gls_path_S0_Z_66a47733f2164099; assign __gls_path_S0_Z_any = __gls_path_S0_Z_edd38b5397ef7ab0; assign __gls_path_S0_Z_any = __gls_path_S0_Z_55b7162a8a034075; wire __gls_path_S0_Z_fallback; assign __gls_path_S0_Z_fallback = (__gls_path_S0_Z_any === 1'b0); wand __gls_path_S1_Z_d06ffbb6a44b42c1; assign __gls_path_S1_Z_d06ffbb6a44b42c1 = (I0 === 1'b0); assign __gls_path_S1_Z_d06ffbb6a44b42c1 = (I1 === 1'b1); assign __gls_path_S1_Z_d06ffbb6a44b42c1 = (I2 === 1'b0); assign __gls_path_S1_Z_d06ffbb6a44b42c1 = (I3 === 1'b0); assign __gls_path_S1_Z_d06ffbb6a44b42c1 = (S0 === 1'b1); wand __gls_path_S1_Z_25d2607013f092a7; assign __gls_path_S1_Z_25d2607013f092a7 = (I0 === 1'b0); assign __gls_path_S1_Z_25d2607013f092a7 = (I1 === 1'b1); assign __gls_path_S1_Z_25d2607013f092a7 = (I2 === 1'b1); assign __gls_path_S1_Z_25d2607013f092a7 = (I3 === 1'b0); assign __gls_path_S1_Z_25d2607013f092a7 = (S0 === 1'b1); wand __gls_path_S1_Z_d755ff127f876a46; assign __gls_path_S1_Z_d755ff127f876a46 = (I0 === 1'b1); assign __gls_path_S1_Z_d755ff127f876a46 = (I1 === 1'b0); assign __gls_path_S1_Z_d755ff127f876a46 = (I2 === 1'b0); assign __gls_path_S1_Z_d755ff127f876a46 = (I3 === 1'b0); assign __gls_path_S1_Z_d755ff127f876a46 = (S0 === 1'b0); wand __gls_path_S1_Z_eb25fdcc57254be2; assign __gls_path_S1_Z_eb25fdcc57254be2 = (I0 === 1'b1); assign __gls_path_S1_Z_eb25fdcc57254be2 = (I1 === 1'b0); assign __gls_path_S1_Z_eb25fdcc57254be2 = (I2 === 1'b0); assign __gls_path_S1_Z_eb25fdcc57254be2 = (I3 === 1'b1); assign __gls_path_S1_Z_eb25fdcc57254be2 = (S0 === 1'b0); wand __gls_path_S1_Z_29c6fce254afda1a; assign __gls_path_S1_Z_29c6fce254afda1a = (I0 === 1'b1); assign __gls_path_S1_Z_29c6fce254afda1a = (I1 === 1'b1); assign __gls_path_S1_Z_29c6fce254afda1a = (I2 === 1'b0); assign __gls_path_S1_Z_29c6fce254afda1a = (I3 === 1'b0); assign __gls_path_S1_Z_29c6fce254afda1a = (S0 === 1'b0); wand __gls_path_S1_Z_87f18acd8aed920d; assign __gls_path_S1_Z_87f18acd8aed920d = (I0 === 1'b1); assign __gls_path_S1_Z_87f18acd8aed920d = (I1 === 1'b1); assign __gls_path_S1_Z_87f18acd8aed920d = (I2 === 1'b0); assign __gls_path_S1_Z_87f18acd8aed920d = (I3 === 1'b0); assign __gls_path_S1_Z_87f18acd8aed920d = (S0 === 1'b1); wand __gls_path_S1_Z_75cc18013c4031a9; assign __gls_path_S1_Z_75cc18013c4031a9 = (I0 === 1'b1); assign __gls_path_S1_Z_75cc18013c4031a9 = (I1 === 1'b1); assign __gls_path_S1_Z_75cc18013c4031a9 = (I2 === 1'b0); assign __gls_path_S1_Z_75cc18013c4031a9 = (I3 === 1'b1); assign __gls_path_S1_Z_75cc18013c4031a9 = (S0 === 1'b0); wand __gls_path_S1_Z_4aebeed0436181c0; assign __gls_path_S1_Z_4aebeed0436181c0 = (I0 === 1'b1); assign __gls_path_S1_Z_4aebeed0436181c0 = (I1 === 1'b1); assign __gls_path_S1_Z_4aebeed0436181c0 = (I2 === 1'b1); assign __gls_path_S1_Z_4aebeed0436181c0 = (I3 === 1'b0); assign __gls_path_S1_Z_4aebeed0436181c0 = (S0 === 1'b1); wand __gls_path_S1_Z_3adb39eda25657c3; assign __gls_path_S1_Z_3adb39eda25657c3 = (I0 === 1'b0); assign __gls_path_S1_Z_3adb39eda25657c3 = (I1 === 1'b0); assign __gls_path_S1_Z_3adb39eda25657c3 = (I2 === 1'b0); assign __gls_path_S1_Z_3adb39eda25657c3 = (I3 === 1'b1); assign __gls_path_S1_Z_3adb39eda25657c3 = (S0 === 1'b1); wand __gls_path_S1_Z_d8f459cefc9aea2c; assign __gls_path_S1_Z_d8f459cefc9aea2c = (I0 === 1'b0); assign __gls_path_S1_Z_d8f459cefc9aea2c = (I1 === 1'b0); assign __gls_path_S1_Z_d8f459cefc9aea2c = (I2 === 1'b1); assign __gls_path_S1_Z_d8f459cefc9aea2c = (I3 === 1'b0); assign __gls_path_S1_Z_d8f459cefc9aea2c = (S0 === 1'b0); wand __gls_path_S1_Z_93c5d1be4afa9dea; assign __gls_path_S1_Z_93c5d1be4afa9dea = (I0 === 1'b0); assign __gls_path_S1_Z_93c5d1be4afa9dea = (I1 === 1'b0); assign __gls_path_S1_Z_93c5d1be4afa9dea = (I2 === 1'b1); assign __gls_path_S1_Z_93c5d1be4afa9dea = (I3 === 1'b1); assign __gls_path_S1_Z_93c5d1be4afa9dea = (S0 === 1'b0); wand __gls_path_S1_Z_3f70607dd1da96f4; assign __gls_path_S1_Z_3f70607dd1da96f4 = (I0 === 1'b0); assign __gls_path_S1_Z_3f70607dd1da96f4 = (I1 === 1'b0); assign __gls_path_S1_Z_3f70607dd1da96f4 = (I2 === 1'b1); assign __gls_path_S1_Z_3f70607dd1da96f4 = (I3 === 1'b1); assign __gls_path_S1_Z_3f70607dd1da96f4 = (S0 === 1'b1); wand __gls_path_S1_Z_b83da87d6aa6ae67; assign __gls_path_S1_Z_b83da87d6aa6ae67 = (I0 === 1'b0); assign __gls_path_S1_Z_b83da87d6aa6ae67 = (I1 === 1'b1); assign __gls_path_S1_Z_b83da87d6aa6ae67 = (I2 === 1'b1); assign __gls_path_S1_Z_b83da87d6aa6ae67 = (I3 === 1'b0); assign __gls_path_S1_Z_b83da87d6aa6ae67 = (S0 === 1'b0); wand __gls_path_S1_Z_d3d57c62117f64a3; assign __gls_path_S1_Z_d3d57c62117f64a3 = (I0 === 1'b0); assign __gls_path_S1_Z_d3d57c62117f64a3 = (I1 === 1'b1); assign __gls_path_S1_Z_d3d57c62117f64a3 = (I2 === 1'b1); assign __gls_path_S1_Z_d3d57c62117f64a3 = (I3 === 1'b1); assign __gls_path_S1_Z_d3d57c62117f64a3 = (S0 === 1'b0); wand __gls_path_S1_Z_991a208764e8d545; assign __gls_path_S1_Z_991a208764e8d545 = (I0 === 1'b1); assign __gls_path_S1_Z_991a208764e8d545 = (I1 === 1'b0); assign __gls_path_S1_Z_991a208764e8d545 = (I2 === 1'b0); assign __gls_path_S1_Z_991a208764e8d545 = (I3 === 1'b1); assign __gls_path_S1_Z_991a208764e8d545 = (S0 === 1'b1); wand __gls_path_S1_Z_daf7190eb2c6ddcc; assign __gls_path_S1_Z_daf7190eb2c6ddcc = (I0 === 1'b1); assign __gls_path_S1_Z_daf7190eb2c6ddcc = (I1 === 1'b0); assign __gls_path_S1_Z_daf7190eb2c6ddcc = (I2 === 1'b1); assign __gls_path_S1_Z_daf7190eb2c6ddcc = (I3 === 1'b1); assign __gls_path_S1_Z_daf7190eb2c6ddcc = (S0 === 1'b1); wor __gls_path_S1_Z_any; assign __gls_path_S1_Z_any = __gls_path_S1_Z_d06ffbb6a44b42c1; assign __gls_path_S1_Z_any = __gls_path_S1_Z_25d2607013f092a7; assign __gls_path_S1_Z_any = __gls_path_S1_Z_d755ff127f876a46; assign __gls_path_S1_Z_any = __gls_path_S1_Z_eb25fdcc57254be2; assign __gls_path_S1_Z_any = __gls_path_S1_Z_29c6fce254afda1a; assign __gls_path_S1_Z_any = __gls_path_S1_Z_87f18acd8aed920d; assign __gls_path_S1_Z_any = __gls_path_S1_Z_75cc18013c4031a9; assign __gls_path_S1_Z_any = __gls_path_S1_Z_4aebeed0436181c0; assign __gls_path_S1_Z_any = __gls_path_S1_Z_3adb39eda25657c3; assign __gls_path_S1_Z_any = __gls_path_S1_Z_d8f459cefc9aea2c; assign __gls_path_S1_Z_any = __gls_path_S1_Z_93c5d1be4afa9dea; assign __gls_path_S1_Z_any = __gls_path_S1_Z_3f70607dd1da96f4; assign __gls_path_S1_Z_any = __gls_path_S1_Z_b83da87d6aa6ae67; assign __gls_path_S1_Z_any = __gls_path_S1_Z_d3d57c62117f64a3; assign __gls_path_S1_Z_any = __gls_path_S1_Z_991a208764e8d545; assign __gls_path_S1_Z_any = __gls_path_S1_Z_daf7190eb2c6ddcc; wire __gls_path_S1_Z_fallback; assign __gls_path_S1_Z_fallback = (__gls_path_S1_Z_any === 1'b0);
   specify

	// specify_block_begin

	if (__gls_path_I0_Z_8424b6dbc4680811) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_83191c966c6bd00e) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_b39edf9ea62c935a) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_9f9cfb3ff7f8f549) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_4d79bffca87523db) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_7bd67582ae5bebe5) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_41238af02176fcc7) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_1123258cc126892e) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I0_Z_fallback) (I0 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_e833a296af4d937f) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_dd6ae494df461d4b) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_7cbec624fd6405ec) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_c4da6787f333b0d9) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_98bc95088385fdcd) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_4383d1922b09e632) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_d1d9599cb6edef01) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_166fc1a64d1b4a5d) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I1_Z_fallback) (I1 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_8b9df3811a837233) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_6e14929d86731def) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_20e72c62277d77eb) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_13b58e70d7e1ef98) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_1c4766127897e6db) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_01b7b437d913054d) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_8f3bdd1eb1a0c93f) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_554dcf7858300e77) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I2_Z_fallback) (I2 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_0a58f28ebd63d02b) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_0daf45bc27540240) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_76d4c04a0abdc208) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_6acbb16535a1e437) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_9f812ef8ee180d3d) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_e4c2c1ade9b4492a) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_68582c3e98962e4c) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_378b8deebd8c3b7d) (I3 => Z) = (1.0,1.0);



	if (__gls_path_I3_Z_fallback) (I3 => Z) = (1.0,1.0);



	if (__gls_path_S0_Z_5d98abc676625da0) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_5d98abc676625da0) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_ff4583194436cdf2) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_ff4583194436cdf2) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_7af0c6f2bcc175a8) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_7af0c6f2bcc175a8) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_24cecb18cd43c5c0) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_24cecb18cd43c5c0) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_6a3c1955b4a12a06) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_6a3c1955b4a12a06) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_0366c29772b1d9e0) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_0366c29772b1d9e0) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_984ead1fbe50c218) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_984ead1fbe50c218) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_4e2b01c2992e2c7a) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_4e2b01c2992e2c7a) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_fallback) (posedge S0 => (Z : S0)) = (1.0,1.0);



	if (__gls_path_S0_Z_fallback) (negedge S0 => (Z : S0)) = (1.0,1.0);



	if (__gls_path_S0_Z_4bf5f7f930cd881b) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_4bf5f7f930cd881b) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_fbae8866159e5dd6) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_fbae8866159e5dd6) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_fbbdc4496fadfc31) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_fbbdc4496fadfc31) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_42ae265a4bafd07f) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_42ae265a4bafd07f) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_9c78918d92ffb60d) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_9c78918d92ffb60d) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_66a47733f2164099) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_66a47733f2164099) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_edd38b5397ef7ab0) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_edd38b5397ef7ab0) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S0_Z_55b7162a8a034075) (posedge S0 => (Z : S0)) = (1.0,1.0);
if (__gls_path_S0_Z_55b7162a8a034075) (negedge S0 => (Z : S0)) = (1.0,1.0);


	if (__gls_path_S1_Z_d06ffbb6a44b42c1) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_d06ffbb6a44b42c1) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_25d2607013f092a7) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_25d2607013f092a7) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_d755ff127f876a46) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_d755ff127f876a46) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_eb25fdcc57254be2) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_eb25fdcc57254be2) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_29c6fce254afda1a) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_29c6fce254afda1a) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_87f18acd8aed920d) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_87f18acd8aed920d) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_75cc18013c4031a9) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_75cc18013c4031a9) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_4aebeed0436181c0) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_4aebeed0436181c0) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_fallback) (posedge S1 => (Z : S1)) = (1.0,1.0);



	if (__gls_path_S1_Z_fallback) (negedge S1 => (Z : S1)) = (1.0,1.0);



	if (__gls_path_S1_Z_3adb39eda25657c3) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_3adb39eda25657c3) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_d8f459cefc9aea2c) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_d8f459cefc9aea2c) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_93c5d1be4afa9dea) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_93c5d1be4afa9dea) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_3f70607dd1da96f4) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_3f70607dd1da96f4) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_b83da87d6aa6ae67) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_b83da87d6aa6ae67) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_d3d57c62117f64a3) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_d3d57c62117f64a3) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_991a208764e8d545) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_991a208764e8d545) (negedge S1 => (Z : S1)) = (1.0,1.0);


	if (__gls_path_S1_Z_daf7190eb2c6ddcc) (posedge S1 => (Z : S1)) = (1.0,1.0);
if (__gls_path_S1_Z_daf7190eb2c6ddcc) (negedge S1 => (Z : S1)) = (1.0,1.0);


	// specify_block_end

   endspecify

   `endif

endmodule
