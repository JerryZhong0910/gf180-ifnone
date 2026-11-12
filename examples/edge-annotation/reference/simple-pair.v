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

module gf180mcu_fd_sc_mcu7t5v0__mux2_2( Z, I1, S, I0 );
input I0, I1, S;
output Z;

   `ifdef FUNCTIONAL  //  functional //

	gf180mcu_fd_sc_mcu7t5v0__mux2_2_func gf180mcu_fd_sc_mcu7t5v0__mux2_2_behav_inst(.Z(Z),.I1(I1),.S(S),.I0(I0));

   `else

	gf180mcu_fd_sc_mcu7t5v0__mux2_2_func gf180mcu_fd_sc_mcu7t5v0__mux2_2_inst(.Z(Z),.I1(I1),.S(S),.I0(I0));

	// spec_gates_begin


	// spec_gates_end



   wand __gls_path_I0_Z_3235b9e3e2cc8771;
   assign __gls_path_I0_Z_3235b9e3e2cc8771 = (I1 === 1'b0);
   wand __gls_path_I0_Z_4d4772acaeb8e908;
   assign __gls_path_I0_Z_4d4772acaeb8e908 = (I1 === 1'b1);
   wor __gls_path_I0_Z_any;
   assign __gls_path_I0_Z_any = __gls_path_I0_Z_3235b9e3e2cc8771;
   assign __gls_path_I0_Z_any = __gls_path_I0_Z_4d4772acaeb8e908;
   wire __gls_path_I0_Z_fallback;
   assign __gls_path_I0_Z_fallback = (__gls_path_I0_Z_any === 1'b0);
   wand __gls_path_I1_Z_835cf1eec13ef5b2;
   assign __gls_path_I1_Z_835cf1eec13ef5b2 = (I0 === 1'b0);
   wand __gls_path_I1_Z_e60879f3ff0ab737;
   assign __gls_path_I1_Z_e60879f3ff0ab737 = (I0 === 1'b1);
   wor __gls_path_I1_Z_any;
   assign __gls_path_I1_Z_any = __gls_path_I1_Z_835cf1eec13ef5b2;
   assign __gls_path_I1_Z_any = __gls_path_I1_Z_e60879f3ff0ab737;
   wire __gls_path_I1_Z_fallback;
   assign __gls_path_I1_Z_fallback = (__gls_path_I1_Z_any === 1'b0);

   specify

	// specify_block_begin

	if (__gls_path_I0_Z_3235b9e3e2cc8771) (I0 => Z) = (1.0,1.0);

	if (__gls_path_I0_Z_4d4772acaeb8e908) (I0 => Z) = (1.0,1.0);

	if (__gls_path_I0_Z_fallback) (I0 => Z) = (1.0,1.0);

	if (__gls_path_I1_Z_835cf1eec13ef5b2) (I1 => Z) = (1.0,1.0);

	if (__gls_path_I1_Z_e60879f3ff0ab737) (I1 => Z) = (1.0,1.0);

	if (__gls_path_I1_Z_fallback) (I1 => Z) = (1.0,1.0);

	(S => Z) = (1.0,1.0);

	(S => Z) = (1.0,1.0);

	// specify_block_end

   endspecify

   `endif

endmodule
