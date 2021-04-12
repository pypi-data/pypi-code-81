        if self.p_mux:
            mid = self.p_mux.m_id
        for i in range(p_len):
            if self.p_mux:
                m.d.comb += p_valid_i[i].eq(0)
                m.d.comb += self.p[i].ready_o.eq(0)
            else:
                m.d.comb += p_valid_i[i].eq(self.p[i].valid_i_logic())
                m.d.comb += self.p[i].ready_o.eq(~data_valid[i] | \
                                                  self.n[ni].ready_i)
                m.d.comb += self.n[ni].valid_o.eq(data_valid[i])
        if self.p_mux:
            m.d.comb += p_valid_i[mid].eq(self.p_mux.active)
            m.d.comb += self.p[mid].ready_o.eq(~data_valid[mid] | \
                                              self.n[ni].ready_i)
            m.d.comb += self.n[ni].valid_o.eq(data_valid[mid])

        for i in range(p_len):
            m.d.comb += n_ready_in[i].eq(~self.n[ni].ready_i & data_valid[i])
            m.d.sync += data_valid[i].eq(p_valid_i[i] | \
                                        (n_ready_in[i] & data_valid[i]))
            with m.If(self.p[i].valid_i & self.p[i].ready_o):
                m.d.sync += eq(r_data[i], self.p[i].data_i)

        if self.p_mux:
            m.d.comb += eq(self.n[ni].data_o,
                           self.stage.process(r_data[mid]))
        else:
            m.d.comb += eq(self.n[ni].data_o, self.stage.process(r_data[i]))
        return m

[A[2~[2~
