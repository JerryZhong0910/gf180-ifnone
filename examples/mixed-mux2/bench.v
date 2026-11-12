// SPDX-License-Identifier: Apache-2.0
`timescale 1ns/1ps
`include "helper.v"
`include "model.v"
`timescale 1ps/1ps
module bench;
  reg s,i0,i1;
  wire z;
  gf180mcu_fd_sc_mcu7t5v0__mux2_2 mux(.S(s),.I0(i0),.I1(i1),.Z(z));
  initial begin
    $sdf_annotate_initial("converted.sdf", bench);
    $path_snapshot("final", mux);
    $display("ANNOTATION_RETURNED %0d",$time);
    #1000; s=0; i0=0; i1=1;
    #9000; s=1;
    #10000; s=0;
    #10000; i0=1; i1=0;
    #10000; s=1;
    #10000; s=0;
    #10000; i0=0;
    #10000; i0=1;
    #10000; i0=0;
    #10000; s=1;
    #10000; i1=1;
    #10000; i1=0;
    #10000; $display("END %0d",$time);
  end
  always @(z) $display("PIN Z %0d %b",$time,z);
  always @(s) $strobe("SOURCE S %0d %b",$time,s);
  always @(i0) $strobe("SOURCE I0 %0d %b",$time,i0);
  always @(i1) $strobe("SOURCE I1 %0d %b",$time,i1);
endmodule
