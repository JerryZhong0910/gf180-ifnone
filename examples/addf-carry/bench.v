`timescale 1ns/1ps
`include "helper.v"
`include "model.v"
module bench;
reg A,B,CI;wire S,CO;
gf180mcu_fd_sc_mcu9t5v0__addf_1 dut(.A(A),.B(B),.CI(CI),.S(S),.CO(CO));
initial begin
$sdf_annotate_initial("converted.sdf",dut);
$path_snapshot("final",dut);
#1 A=0;B=0;CI=1;
#9 A=1;
#10 A=0;
#10 $display("END %0d",$time*1000);$finish;
end
always @(CO) $display("PIN CO %0d %b",$realtime*1000,CO);
endmodule
