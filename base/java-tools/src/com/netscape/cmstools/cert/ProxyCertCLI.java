// --- BEGIN COPYRIGHT BLOCK ---
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; version 2 of the License.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
// (C) 2018 Red Hat, Inc.
// All rights reserved.
// --- END COPYRIGHT BLOCK ---

package com.netscape.cmstools.cert;

import com.netscape.cmstools.ca.CACertCLI;
import com.netscape.cmstools.cli.CLI;
import com.netscape.cmstools.cli.ProxyCLI;

/**
 * @deprecated pki cert has been deprecated. Use pki ca-cert instead.
 */
@Deprecated
public class ProxyCertCLI extends ProxyCLI {

    public ProxyCertCLI(CLI parent) {
        super(new CACertCLI(parent), "ca");
    }

    public void execute(String[] args) throws Exception {
        System.err.println("WARNING: pki cert has been deprecated. Use pki ca-cert instead.");
        super.execute(args);
    }
}
